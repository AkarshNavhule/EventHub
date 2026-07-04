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

## Postman ScreenShots

Events

<img width="710" height="518" alt="image" src="https://github.com/user-attachments/assets/a8268dc4-eb70-46c2-b216-507957dfa72c" />
<img width="713" height="542" alt="image" src="https://github.com/user-attachments/assets/460ff6aa-c0dc-46b4-82f2-ed19e373a752" />
<img width="714" height="546" alt="image" src="https://github.com/user-attachments/assets/99a5f4a2-9177-4e4b-9719-a87779a7a341" />
<img width="713" height="548" alt="image" src="https://github.com/user-attachments/assets/2b504367-a614-431c-8a7d-bf976e5c9a74" />
<img width="711" height="540" alt="image" src="https://github.com/user-attachments/assets/b5993a36-2f18-4e6f-aa72-fddef2049fc2" />
<img width="710" height="547" alt="image" src="https://github.com/user-attachments/assets/785b77bd-da99-4192-b270-5ccd6d4ad416" />
<img width="715" height="545" alt="image" src="https://github.com/user-attachments/assets/f461b698-51ca-443d-8918-b9f758b8a0d6" />

Reservations

<img width="713" height="544" alt="image" src="https://github.com/user-attachments/assets/983013c5-8fa5-4a5e-8e6a-c2c85d4c8997" />
<img width="710" height="543" alt="image" src="https://github.com/user-attachments/assets/1b4fcdba-85ac-462e-baa8-97e792fdf266" />
<img width="710" height="524" alt="image" src="https://github.com/user-attachments/assets/3ba16ab0-a152-4704-943f-b5d42bf6aeb1" />
<img width="714" height="544" alt="image" src="https://github.com/user-attachments/assets/b0ba9af1-3d0b-4106-9bd9-e9e6779003d7" />
<img width="710" height="542" alt="image" src="https://github.com/user-attachments/assets/9f695f0c-7987-4a58-be85-57f36c620436" />
<img width="707" height="546" alt="image" src="https://github.com/user-attachments/assets/44c21f0e-6b20-4ccf-961e-eb9d40a6b6e8" />








