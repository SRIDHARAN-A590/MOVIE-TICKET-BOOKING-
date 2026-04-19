# Movie Ticket Booking System

A full-stack Movie Ticket Booking System built with HTML/CSS/JS (Frontend), Python Flask (Backend), and MySQL (Database).

## Prerequisites
- Python 3.8+
- MySQL Server
- Node.js (Optional, usually for frontend servers but you can just use Live Server)

## Setup Instructions

### 1. Database Setup (MySQL)
1. Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or CLI).
2. Execute the `backend/database/schema.sql` completely. It contains the logic for creating tables, triggers, functions, stored procedures, and views.
3. Execute the `backend/database/seed.sql` to populate dummy movies, theatres, shows, and seats so you can test out the UI immediately.

### 2. Backend Setup (Flask)
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update the DB credentials in the `.env` file to match your local MySQL configuration.
5. Run the Flask API server:
   ```bash
   python app.py
   ```
   *The server runs at `http://localhost:5000/api`*

### 3. Frontend Setup
1. You can simply open the `frontend/index.html` file in your browser, or preferrably, use an extension like **Live Server** in VSCode to serve it over a local port (e.g. `http://localhost:5500`).
2. Explore the site, register an account, log in, select seats, and complete bookings!

## Advanced Database Features Used
- **Trigger**: Automatically updates seat status to 'Booked' when a payment/booking completes.
- **Stored Procedure**: Exception handling for invalid bookings.
- **Function**: Calculates dynamic discounts for ticket sales.
- **View**: Consolidates User, Movie, Theatre, and Booking tables for the frontend booking history.
- **Cursor**: Designed inside the procedure to loop through available seats sequentially.
