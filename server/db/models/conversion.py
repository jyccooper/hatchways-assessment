from ..db import db


class Conversion(db.Model):
    __tablename__ = "conversion"

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float, nullable=False)
    from_curr = db.Column(db.String, nullable=False)
    to_curr = db.Column(db.String, nullable=False)

    @staticmethod
    def find_exchange_rate(from_curr, to_curr):
        return Conversion.query.filter(
            Conversion.from_curr == from_curr, Conversion.to_curr == to_curr
        ).first()
