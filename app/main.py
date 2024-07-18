from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
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
        customer_contact = request.form['customer_contact']
        order_items_data = request.form.getlist('order_items')

        total_amount = 0
        new_order = Order(customer_name=customer_name, customer_contact=customer_contact, total_amount=0)
        db.session.add(new_order)
        db.session.commit()  # Commit here to get order_id

        order_items = []
        for menu_item_id in order_items_data:
            quantity = int(request.form.get(f'quantity_{menu_item_id}', 1))
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

        receipt_html = render_template('receipt.html', order=new_order, order_items=order_items)
        return jsonify({'status': 'success', 'receipt_html': receipt_html})

    menu_items = MenuItem.query.filter_by(deleted=False).all()
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

    menu_items = MenuItem.query.filter_by(deleted=False).all()
    return render_template('menu.html', menu_items=menu_items)

@main.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        print(f"Attempting to soft delete item with id: {item_id}")
        item.deleted = True
        db.session.commit()
        flash('Menu item removed from menu successfully!', 'success')
    else:
        print("Item not found.")
        flash('Menu item not found.', 'danger')
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
    orders = Order.query.order_by(Order.datetime.desc()).all()
    return render_template('order_history.html', orders=orders)

################################################################################################
@main.route('/manage_expenditures', methods=['GET', 'POST'])
def manage_expenditures():
    if request.method == 'POST':
        print("Received POST request")
        if request.is_json:
            data = request.get_json()
            print("JSON data received:", data)
            if 'add_modify_expenditure' in data:
                print("Add/Modify Expenditure action triggered")
                description = data['description']
                amount = float(data['amount'])
                year = int(data['year'])
                month = int(data['month'])
                expenditure = Expenditure.query.filter_by(description=description, year=year, month=month).first()
                if expenditure:
                    print("Updating existing expenditure")
                    expenditure.amount = amount
                else:
                    print("Adding new expenditure")
                    expenditure = Expenditure(description=description, amount=amount, year=year, month=month)
                    db.session.add(expenditure)
                db.session.commit()
                expenditures = Expenditure.query.filter_by(year=year, month=month).all()
                expenditures_data = [{'id': exp.id, 'description': exp.description, 'amount': exp.amount} for exp in expenditures]
                print("Expenditures after add/modify:", expenditures_data)
                return jsonify({'status': 'success', 'message': 'Expenditure added/modified successfully!', 'expenditures': expenditures_data})

            elif 'remove_expenditure' in data:
                print("Remove Expenditure action triggered")
                expenditure_id = int(data['expenditure_id'])
                expenditure = Expenditure.query.get(expenditure_id)
                if expenditure:
                    db.session.delete(expenditure)
                    db.session.commit()
                year = int(data['year'])
                month = int(data['month'])
                expenditures = Expenditure.query.filter_by(year=year, month=month).all()
                expenditures_data = [{'id': exp.id, 'description': exp.description, 'amount': exp.amount} for exp in expenditures]
                print("Expenditures after remove:", expenditures_data)
                return jsonify({'status': 'success', 'message': 'Expenditure removed successfully!', 'expenditures': expenditures_data})

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        print("GET request for year:", year, "month:", month)
        expenditures = Expenditure.query.filter_by(year=year, month=month).all()
        expenditures_data = [{'id': exp.id, 'description': exp.description, 'amount': exp.amount} for exp in expenditures]
        print("Expenditures for GET request:", expenditures_data)
        return jsonify({'expenditures': expenditures_data})

    return render_template('manage_expenditures.html', datetime=datetime, calendar=calendar)

################################################################################################
@main.route('/financial_report', methods=['GET', 'POST'])
def financial_report():
    selected_year = None
    selected_months = []
    expenditures = Expenditure.query.all()

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'generate_report' in data:
                selected_year = int(data['year'])
                selected_months = [int(month) for month in data['months']]
                return generate_report(selected_year, selected_months)
                
    return render_template('financial_report.html', datetime=datetime, calendar=calendar)

@main.route('/generate_report', methods=['POST'])
def generate_report(selected_year=None, selected_months=None):
    if not selected_year or not selected_months:
        data = request.get_json()
        selected_year = int(data['year'])
        selected_months = [int(month) for month in data['months']]
    
    selected_dates = [datetime(selected_year, month, 1) for month in selected_months]
    selected_month_names = [calendar.month_name[month] for month in selected_months]

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

    total_salaries = sum(employee.salary * len(selected_months) for employee in Employee.query.all())

    expenditures = Expenditure.query.filter(Expenditure.year == selected_year, Expenditure.month.in_(selected_months)).all()
    other_expenditures = sum(exp.amount for exp in expenditures)
    expenditure_details = [{'description': exp.description, 'amount': exp.amount, 'year': exp.year, 'month': exp.month} for exp in expenditures]

    total_expenditures = total_salaries + other_expenditures
    total_profit = total_sales - total_cost - total_expenditures

    report_data = {
        'total_sales': total_sales,
        'total_cost': total_cost,
        'total_salaries': total_salaries,
        'other_expenditures': other_expenditures,
        'expenditure_details': expenditure_details,
        'total_profit': total_profit,
        'selected_year': selected_year,
        'selected_months': selected_month_names
    }

    session['report_data'] = report_data
    return jsonify({'status': 'success', 'redirect_url': url_for('main.display_report')})

@main.route('/display_report')
def display_report():
    report_data = session.get('report_data')
    return render_template('report.html', report=report_data)