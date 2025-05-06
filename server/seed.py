import os
import json
from pathlib import Path
from flask import Flask
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError

from db.db import db
from db.models.conversion import Conversion
from db.models.transaction import Transaction


def create_app():
    app = Flask(__name__)
    database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_PATH", f"sqlite:///{database_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def reset(db):
    try:
        Conversion.__table__.drop(db.engine)
        Transaction.__table__.drop(db.engine)
    except SQLAlchemyError as e:
        print(f"There was an error dropping the tables: {e}")
        pass
    db.create_all()
    print("db is reset!")


def get_latest_transaction_date(transactions):
    date_format = "%Y-%m-%d %H:%M:%S"

    latest_date_found = datetime.strptime(transactions[0]["date"], date_format)

    for transaction in transactions:
        if datetime.strptime(transaction["date"], date_format) > latest_date_found:
            latest_date_found = datetime.strptime(transaction["date"], date_format)

    return latest_date_found


def seed(db, time_for_seeding):
    current_dir = Path(__file__).parent

    transactions_path = current_dir.joinpath("db/seed_data/transactions.json")
    conversions_path = current_dir.joinpath("db/seed_data/conversions.json")

    # Transactions
    with open(transactions_path, "r") as f:
        transactions = json.loads(f.read())["transactions"]

    latest_date_found = get_latest_transaction_date(transactions)

    diff = (time_for_seeding - latest_date_found).days

    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d %H:%M:%S")
        updated_date = transaction_date + timedelta(days=diff)

        new_transaction = Transaction(
            id=transaction["id"],
            amount=transaction["amount"],
            currency=transaction["currency"],
            date=updated_date,
        )
        db.session.add(new_transaction)
        db.session.commit()

    # Conversions
    with open(conversions_path, "r") as f:
        conversions = json.loads(f.read())["conversions"]

    for conversion in conversions:
        new_conversion = Conversion(
            id=conversion["id"],
            from_curr=conversion["from_curr"],
            to_curr=conversion["to_curr"],
            rate=conversion["rate"],
        )
        db.session.add(new_conversion)
        db.session.commit()

    print("seeded transactions and conversions")


if __name__ == "__main__":
    with create_app().app_context():
        db.create_all()
        print("seeding...")
        reset(db)
        seed(db, datetime.now())
