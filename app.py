from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from db import create_table, insert_booking, fetch_all_bookings
from pricing import get_pricing_signal
from analytics import revenue_analytics, demand_by_category


# -------------------
# APP CONFIG
# -------------------

app = Flask(__name__)
CORS(app)

API_KEY = "sciative-demo-key"

# Ensure DB exists
create_table()


# -------------------
# AUTH HELPER
# -------------------

def require_api_key(req):
    key = req.headers.get("X-API-KEY")
    return key == API_KEY


def unauthorized():
    return jsonify({
        "error": "Unauthorized",
        "message": "Invalid or missing API key"
    }), 401


# -------------------
# HOME
# -------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "PriceOptima Booking Pricing API",
        "status": "running"
    })


# -------------------
# CREATE BOOKING (PROTECTED)
# -------------------

@app.route("/booking", methods=["POST"])
def create_booking():

    if not require_api_key(request):
        return unauthorized()

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "InvalidRequest",
            "message": "JSON body required"
        }), 400

    category = data.get("category")
    base_price = data.get("base_price")

    if not isinstance(category, str) or not category.strip():
        return jsonify({
            "error": "ValidationError",
            "field": "category",
            "message": "category must be a non-empty string"
        }), 400

    if not isinstance(base_price, (int, float)) or base_price <= 0:
        return jsonify({
            "error": "ValidationError",
            "field": "base_price",
            "message": "base_price must be a positive number"
        }), 400

    # Pricing logic
    bookings = fetch_all_bookings()
    pricing = get_pricing_signal(bookings)

    final_price = round(base_price * pricing["price_multiplier"], 2)
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        insert_booking(category, base_price, final_price, booking_time)
    except Exception:
        return jsonify({
            "error": "DatabaseError",
            "message": "Failed to store booking"
        }), 500

    return jsonify({
        "status": "success",
        "data": {
            "category": category,
            "base_price": base_price,
            "final_price": final_price,
            "pricing_reason": pricing["reason"],
            "booking_time": booking_time
        }
    }), 201


# -------------------
# GET BOOKINGS (PUBLIC)
# -------------------

@app.route("/bookings", methods=["GET"])
def get_bookings():
    bookings = fetch_all_bookings()
    return jsonify({
        "count": len(bookings),
        "data": bookings
    })


# -------------------
# ANALYTICS: REVENUE (PUBLIC)
# -------------------

@app.route("/analytics/revenue", methods=["GET"])
def revenue():
    bookings = fetch_all_bookings()
    return jsonify(revenue_analytics(bookings))


# -------------------
# ANALYTICS: DEMAND (PUBLIC)
# -------------------

@app.route("/analytics/demand", methods=["GET"])
def demand():
    bookings = fetch_all_bookings()
    return jsonify(demand_by_category(bookings))


# -------------------
# PRICING SIGNAL (PUBLIC)
# -------------------

@app.route("/pricing/signal", methods=["GET"])
def pricing_signal():
    bookings = fetch_all_bookings()
    return jsonify(get_pricing_signal(bookings))


# -------------------
# RUN SERVER
# -------------------

if __name__ == "__main__":
    app.run(debug=True)
