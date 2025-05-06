from flask import jsonify, request
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from api import api
from db.models.transaction import Transaction
from db.models.conversion import Conversion
from utils.helpers import DAILY, resolve_date_range


@api.get("/spendings")
def get_spendings():
    try:
        # Parse and validate parameters
        query_frame = request.args.get("frame", "daily")
        if query_frame not in ["daily", "monthly", "yearly"]:
            query_frame = "daily"
            
        try:
            query_range = max(1, min(6, int(request.args.get("range", 1))))
        except (ValueError, TypeError):
            query_range = 1
            
        query_currency = request.args.get("currency", "CAD")

        # Get date range
        dates = resolve_date_range(query_frame, query_range)

        # Process transactions
        transactions = Transaction.get_transactions_for_range(
            dates["from_date"], dates["to_date"]
        )
        
        grouped_data = {}

        for transaction in transactions:
            try:
                # Convert currency if needed
                amount = float(transaction.amount)
                if transaction.currency and transaction.currency != query_currency:
                    rate = Conversion.find_exchange_rate(
                        transaction.currency, 
                        query_currency
                    )
                    if rate:
                        amount *= float(rate.rate)

                # Group by time frame
                date_key = (
                    transaction.date.strftime("%Y-%m-%d") if query_frame == "daily" else
                    transaction.date.strftime("%Y-%m") if query_frame == "monthly" else
                    transaction.date.strftime("%Y")
                )
                grouped_data[date_key] = grouped_data.get(date_key, 0) + amount

            except (AttributeError, ValueError):
                continue

        # Format response
        response_data = [
            {
                "totalAmount": round(amount, 2),
                "startDate": date_key,
                "currency": query_currency
            }
            for date_key, amount in sorted(grouped_data.items())
        ]

        return jsonify({"spendings": response_data})

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400