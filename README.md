# EventHub API

EventHub is a backend API for a simplified event ticketing platform built with Django REST Framework (DRF).

## How to Run the Project

1. **Clone the repository:**
   `git clone <your-repo-url>`
2. **Navigate to the project directory:**
   `cd eventhub`
3. **Create and activate a virtual environment:**
   `python -m venv env`
   `source env/bin/activate` (Mac/Linux) OR `env\Scripts\activate` (Windows)
4. **Install dependencies:**
   `pip install -r requirements.txt`
5. **Run database migrations:**
   `python manage.py migrate`
6. **Start the development server:**
   `python manage.py runserver`

## API Endpoints

### Events
* `GET /api/events/` : List all events (Supports filtering: `?status=upcoming` & `?venue=Bangalore`).
* `POST /api/events/` : Create a new event.
* `GET /api/events/{id}/` : Retrieve a specific event.

### Reservations
* `GET /api/reservations/` : List all reservations (Supports filtering: `?event_id=1`).
* `POST /api/reservations/` : Reserve seats for an event. Automatically deducts available seats.
* `POST /api/reservations/{id}/cancel/` : Cancel a reservation. Restores the seats back to the event.

## Design Decision

**Decision:** I chose to handle the seat deduction logic inside the `create()` method of the `ReservationSerializer` rather than in the view.
**Why:** This keeps the business logic (data manipulation) tightly coupled with data validation. It ensures that whenever a reservation is successfully validated and saved via the serializer, the event's available seat count is simultaneously updated, keeping our database consistent without cluttering the ViewSet. (Note: In a high-concurrency production environment, this would be wrapped in a `transaction.atomic()` block to prevent race conditions).