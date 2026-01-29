from collections import defaultdict
from datetime import datetime


def revenue_analytics(bookings):
    daily_revenue = defaultdict(float)

    for b in bookings:
        date = b["booking_time"].split(" ")[0]
        daily_revenue[date] += b["final_price"]

    return {
        "daily_revenue": dict(daily_revenue)
    }


def demand_by_category(bookings):
    demand = defaultdict(int)

    for b in bookings:
        demand[b["category"]] += 1

    return dict(demand)
