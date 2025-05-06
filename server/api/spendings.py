from flask import jsonify, request
from datetime import datetime

from api import api
from db.models.transaction import Transaction
from utils.helpers import DAILY, resolve_date_range


@api.get("/spendings")
def get_spendings():
    # Run the `seed` script to refresh your database with transactions closer to-date
    query_params = request.args.to_dict()
    query_frame = query_params.get("frame", DAILY)
    query_range = query_params.get("range", 6)

    dates = resolve_date_range(query_frame, query_range)

    transactions = Transaction.get_transactions_for_range(
        dates["from_date"], dates["to_date"]
    )
    total_amount_dict = {}

    for transaction in transactions:
        # Group transactions per day
        date_string = transaction.date.strftime("%Y-%m-%d")

        if date_string in total_amount_dict:
            total_amount_dict[date_string] += transaction.amount
        else:
            total_amount_dict[date_string] = transaction.amount

    formatted_spending_data = []

    for date in total_amount_dict.keys():
        formatted_spending_data.append(
            {
                "totalAmount": round(total_amount_dict[date], 2),
                "startDate": datetime.fromisoformat(date).isoformat(),
            }
        )

    data = {
        "spendings": sorted(
            formatted_spending_data,
            key=lambda data: datetime.fromisoformat(data["startDate"]),
            reverse=False,
        )
    }

    return jsonify(data)
