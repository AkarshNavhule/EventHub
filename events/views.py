# events/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        # Start with all events
        queryset = Event.objects.all()

        # Read query parameters from the URL (e.g., ?status=upcoming)
        status_param = self.request.query_params.get('status')
        venue_param = self.request.query_params.get('venue')

        # Apply filters if the parameters exist
        if status_param:
            queryset = queryset.filter(status=status_param)
        if venue_param:
            queryset = queryset.filter(venue__icontains=venue_param)  # icontains makes it case-insensitive

        return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()
        event_id = self.request.query_params.get('event_id')

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset

    # @action adds a custom endpoint to this ViewSet. 
    # detail=True means it applies to a specific reservation (e.g., /reservations/1/cancel/)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()

        # Prevent double-cancellation
        if reservation.status == 'cancelled':
            return Response({'error': 'Already cancelled.'}, status=400)

        # Restore the seats to the event
        reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()

        # Update the reservation status
        reservation.status = 'cancelled'
        reservation.save()

        # Return the updated reservation data
        return Response(self.get_serializer(reservation).data)