PriceOptima – Booking & Dynamic Pricing API

PriceOptima is a Flask-based backend system that simulates a real-world booking platform with demand-aware pricing, secure APIs, and analytics dashboards.
The project demonstrates backend engineering fundamentals, modular design, and end-to-end data flow from APIs to visualization.

🚀 Features

Create bookings with API-key authentication

Demand-aware dynamic pricing engine

Revenue and demand analytics endpoints

Lightweight frontend dashboard (HTML + Chart.js)

Modular architecture (pricing, analytics, database layers separated)

Defensive validation and meaningful HTTP status codes

🧱 Tech Stack

Backend: Python, Flask

Database: SQLite

Frontend: HTML, JavaScript, Chart.js

Authentication: API Key

Version Control: Git & GitHub

📊 API Endpoints
1️⃣ Health Check

GET /
Checks whether the API service is running.

2️⃣ Create Booking (Protected)

POST /booking

Headers

X-API-KEY: sciative-demo-key
Content-Type: application/json


Request Body

{
  "category": "luxury_bus",
  "base_price": 1000
}


Response

{
  "status": "success",
  "data": {
    "category": "luxury_bus",
    "base_price": 1000,
    "final_price": 1100,
    "pricing_reason": "High demand",
    "booking_time": "2026-01-30 12:45:10"
  }
}

3️⃣ Get All Bookings

GET /bookings

Returns all stored bookings.

4️⃣ Revenue Analytics

GET /analytics/revenue

Returns aggregated revenue metrics.

5️⃣ Demand by Category

GET /analytics/demand

Returns booking counts grouped by category.

6️⃣ Pricing Signal

GET /pricing/signal

Returns the current pricing multiplier and reasoning.

7️⃣ Analytics Dashboard

GET /dashboard

Displays revenue and demand charts using real backend data.

▶️ How to Run
python app.py


Open dashboard in browser:

http://127.0.0.1:5000/dashboard

🧠 Design Highlights

Separation of read-only analytics from authenticated write operations

Extensible pricing logic without hard-coded rules

Real-time data consumption by frontend dashboard

Backend-first design with clean API contracts

🎯 Use Case

PriceOptima simulates how travel or retail platforms dynamically adjust pricing based on demand and analyze booking trends, making it suitable for backend engineering interviews and internships.

📌 Future Enhancements

JWT-based authentication

Time-series revenue analytics

Surge pricing by time and demand

React-based dashboard

Dockerization

✍️ Author

Harsh Tandel
