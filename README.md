# Restaurant Management System (RMS)

The Restaurant Management System (RMS) is a web-based application designed to streamline the operations of a restaurant. It allows for efficient management of menu items, orders, employees, and financial reports.

## Features

- **Menu Management**: Add, edit, and delete menu items with details such as name, ingredients, price, and cost.
- **Order Management**: Place orders by selecting menu items, specifying quantities, and generating receipts.
- **Employee Management**: Add, edit, and remove employees, and manage employee details such as name, contact, and salary.
- **Financial Reports**: Generate monthly financial reports, including total sales, total costs, salaries, other expenditures, and total profit.
- **Expenditure Management**: Add and manage additional expenditures directly from the financial report page.

## Installation

To install and run the RMS locally, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/rms.git
    cd rms
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**

    ```bash
    flask shell
    ```

    In the Flask shell, run the following commands:

    ```python
    from app import create_app
    from app.models import db

    app = create_app()
    with app.app_context():
        db.create_all()
    ```

5. **Run the Application**

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000/`.

## Usage

### Menu Management

- Navigate to the **Menu** page to add, edit, or delete menu items.

### Order Management

- Navigate to the **Orders** page to place new orders. Select menu items, specify quantities, and generate receipts.

### Employee Management

- Navigate to the **Employees** page to add, edit, or remove employees.

### Financial Reports

- Navigate to the **Financial Report** page to generate monthly financial reports. Select the financial year and months to generate a report. Add additional expenditures if necessary.

## Project Structure

Restaurant Management System (RMS)/
├── app/
│ ├── init.py
│ ├── auth.py
│ ├── main.py
│ ├── models.py
│ ├── templates/
│ │ ├── index.html
│ │ ├── orders.html
│ │ ├── order_history.html
│ │ ├── menu.html
│ │ ├── employees.html
│ │ ├── financial_report.html
│ ├── static/
│ │ ├── css/
│ │ │ ├── index.css
│ │ │ ├── orders.css
│ │ │ ├── menu.css
│ │ │ ├── employees.css
│ │ │ ├── financial_report.css
├── instances/restaurant.db
├── run.py
├── requirements.txt
└── README.md


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Bootstrap: [https://getbootstrap.com/](https://getbootstrap.com/)
- Font Awesome: [https://fontawesome.com/](https://fontawesome.com/)
