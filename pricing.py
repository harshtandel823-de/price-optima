from datetime import datetime, timedelta


def get_pricing_signal(bookings):
    """
    Simple demand-based pricing logic.
    If more than 5 bookings happened in last 60 minutes,
    apply surge pricing.
    """

    now = datetime.now()
    one_hour_ago = now - timedelta(minutes=60)

    recent_bookings = []

    for booking in bookings:
        booking_time = datetime.strptime(
            booking["booking_time"], "%Y-%m-%d %H:%M:%S"
        )

        if booking_time >= one_hour_ago:
            recent_bookings.append(booking)

    if len(recent_bookings) > 5:
        return {
            "demand": "high",
            "price_multiplier": 1.1,
            "reason": "High booking volume in last 60 minutes"
        }

    return {
        "demand": "normal",
        "price_multiplier": 1.0,
        "reason": "Normal demand"
    }
