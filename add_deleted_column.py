
from app import create_app
from app.models import db
from sqlalchemy import text

def add_deleted_column():
    app = create_app()
    
    with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(text('ALTER TABLE menu_item ADD COLUMN deleted BOOLEAN DEFAULT FALSE NOT NULL'))
        db.session.commit()
        print("Added 'deleted' column to the menu_item table.")

if __name__ == "__main__":
    add_deleted_column()