from ..db import db


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=False)

    @staticmethod
    def get_transactions_for_range(from_date, to_date):
        return Transaction.query.filter(
            Transaction.date >= from_date.date(), Transaction.date <= to_date.date()
        ).all()
