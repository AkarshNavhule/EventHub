# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ReservationViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'events', EventViewSet, basename='event')
router.register(r'reservations', ReservationViewSet, basename='reservation')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]