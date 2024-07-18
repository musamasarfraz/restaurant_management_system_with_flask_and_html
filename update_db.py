# # update_db.py

# from app import create_app, db
# from app.models import Order

# # Initialize the Flask application
# app = create_app()

# with app.app_context():
#     # Add the new column to the Order model if it doesn't already exist
#     if not hasattr(Order, 'customer_contact'):
#         from sqlalchemy import Column, String

#         # Add the new column to the database
#         with db.engine.connect() as connection:
#             connection.execute('ALTER TABLE order ADD COLUMN customer_contact VARCHAR(100)')

#         # Reflect the new changes in the SQLAlchemy model
#         db.reflect()

#     # Optionally, you can add more logic here to update existing records or other database operations

#     print("Database updated successfully.")
