from flask import Blueprint

auth = Blueprint('auth', __name__)

# Define your authentication routes here
@auth.route('/login')
def login():
    return "Login Page"
