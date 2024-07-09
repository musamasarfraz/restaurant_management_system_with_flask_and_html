from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, MenuItem, Order, OrderItem, Employee, Expenditure
from datetime import datetime
import calendar
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
####################################################################
@main.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        order_items_data = request.form.getlist('order_items')
        quantities = request.form.getlist('quantity')
        
        total_amount = 0
        new_order = Order(customer_name=customer_name, total_amount=0)
        db.session.add(new_order)
        db.session.commit()  # Commit here to get order_id

        order_items = []
        for i in range(len(order_items_data)):
            menu_item_id = int(order_items_data[i])
            quantity = int(quantities[i])
            menu_item = MenuItem.query.get(menu_item_id)
            if menu_item:
                price = menu_item.price * quantity
                total_amount += price
                new_order_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    price=price
                )
                db.session.add(new_order_item)
                order_items.append({
                    'name': menu_item.name,
                    'quantity': quantity,
                    'price': price
                })

        new_order.total_amount = total_amount
        db.session.commit()
        
        flash('Order sent to kitchen. Printing Receipt.', 'success')
        return render_template('receipt.html', order=new_order, order_items=order_items)

    menu_items = MenuItem.query.all()
    return render_template('orders.html', menu_items=menu_items)
####################################################################

@main.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        price = float(request.form['price'])
        cost = float(request.form['cost'])

        new_item = MenuItem(name=name, ingredients=ingredients, price=price, cost=cost)
        db.session.add(new_item)
        db.session.commit()
        flash('New menu item added successfully!', 'success')
        return redirect(url_for('main.menu'))

    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu_items=menu_items)

@main.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Menu item deleted successfully!', 'success')
    return redirect(url_for('main.menu'))


####################################################################


@main.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        if 'add_employee' in request.form:
            name = request.form['name']
            contact = request.form['contact']
            salary = float(request.form['salary'])

            new_employee = Employee(name=name, contact=contact, salary=salary)
            db.session.add(new_employee)
            db.session.commit()
            flash('New employee added successfully!', 'success')
        elif 'remove_employee' in request.form:
            employee_id = int(request.form['employee_id'])
            employee = Employee.query.get(employee_id)
            if employee:
                db.session.delete(employee)
                db.session.commit()
                flash('Employee removed successfully!', 'success')

    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)
################################################################################################

@main.route('/order_history', methods=['GET'])
def sales():
    orders = Order.query.all()
    return render_template('order_history.html', orders=orders)

################################################################################################

@main.route('/financial_report', methods=['GET', 'POST'])
def financial_report():
    if request.method == 'POST':
        if 'add_expenditure' in request.form:
            name = request.form['name']
            amount = float(request.form['amount'])
            date = datetime.now()

            new_expenditure = Expenditure(name=name, amount=amount, date=date)
            db.session.add(new_expenditure)
            db.session.commit()
            flash('New expenditure added successfully!', 'success')
            return redirect(url_for('main.financial_report'))

        elif 'remove_expenditure' in request.form:
            expenditure_id = int(request.form['expenditure_id'])
            expenditure = Expenditure.query.get(expenditure_id)
            if expenditure:
                db.session.delete(expenditure)
                db.session.commit()
                flash('Expenditure removed successfully!', 'success')
            return redirect(url_for('main.financial_report'))

        elif 'generate_report' in request.form:
            selected_year = int(request.form['year'])
            selected_months = request.form.getlist('months')
            selected_dates = [datetime(selected_year, int(month), 1) for month in selected_months]
            selected_month_names = [calendar.month_name[int(month)] for month in selected_months]

            total_sales = 0
            total_cost = 0
            for date in selected_dates:
                start_date = date.replace(day=1)
                end_date = date.replace(day=calendar.monthrange(date.year, date.month)[1])
                orders = Order.query.filter(Order.datetime.between(start_date, end_date)).all()
                for order in orders:
                    total_sales += order.total_amount
                    for item in order.order_items:
                        total_cost += item.menu_item.cost * item.quantity

            total_salaries = sum(employee.salary for employee in Employee.query.all())
            other_expenditures = sum(exp.amount for exp in Expenditure.query.filter(Expenditure.date.between(start_date, end_date)).all())

            total_expenditures = total_salaries + other_expenditures
            total_profit = total_sales - total_cost - total_expenditures

            return render_template('financial_report.html', total_sales=total_sales, total_cost=total_cost,
                                   total_salaries=total_salaries, other_expenditures=other_expenditures,
                                   total_profit=total_profit, selected_year=selected_year, selected_months=selected_month_names,
                                   expenditures=Expenditure.query.all(), datetime=datetime)

    return render_template('financial_report.html', total_sales=None, total_cost=None,
                           total_salaries=None, other_expenditures=None, total_profit=None,
                           selected_year=None, selected_months=None, expenditures=Expenditure.query.all(), datetime=datetime)