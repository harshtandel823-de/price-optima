# Transaction Management API

A simple RESTful backend service built using Flask and SQLite to simulate transaction ingestion and retrieval, inspired by real-world payment processing systems.

## Features
- REST API built with Flask
- SQLite database for persistence
- Add new transactions via POST request
- Fetch all transactions via GET request
- Input validation and proper HTTP status codes

## Tech Stack
- Python
- Flask
- SQLite

## API Endpoints

### 1. Health Check
**GET /**  
Returns a simple message to verify server is running.

### 2. Add Transaction
**POST /transaction**

Request Body:
```json
{
  "amount": 250,
  "type": "debit"
}
