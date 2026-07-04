# events/serializers.py
from rest_framework import serializers
from .models import Event, Reservation


class EventSerializer(serializers.ModelSerializer):
    # This is a computed field. It doesn't exist in the database,
    # but we calculate it on the fly when returning data.
    reservations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'venue', 'date', 'total_seats', 'available_seats', 'status', 'created_at',
                  'reservations_count']

    def get_reservations_count(self, obj):
        # Counts only the 'confirmed' reservations for this specific event
        return obj.reservations.filter(status='confirmed').count()

    def validate(self, data):
        # Object-level validation: ensures available seats make logical sense
        if data.get('available_seats', 0) > data.get('total_seats', 0):
            raise serializers.ValidationError('available_seats cannot exceed total_seats.')
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'event', 'attendee_name', 'attendee_email', 'seats_reserved', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate_seats_reserved(self, value):
        # Field-level validation: ensures they book at least one seat
        if value < 1:
            raise serializers.ValidationError('Must reserve at least 1 seat.')
        return value

    def validate(self, data):
        event = data.get('event')

        # Check if the event is actually open for booking
        if event.status not in ('upcoming', 'ongoing'):
            raise serializers.ValidationError(
                f'Cannot reserve seats for a {event.status} event.'
            )

        # Check for overbooking
        if data.get('seats_reserved', 0) > event.available_seats:
            raise serializers.ValidationError(
                f'Only {event.available_seats} seat(s) available.'
            )
        return data

    def create(self, validated_data):
        # Custom logic during creation:
        # We deduct the requested seats from the event's available_seats here
        event = validated_data['event']
        event.available_seats -= validated_data['seats_reserved']
        event.save()

        # Finally, create and return the Reservation record
        return Reservation.objects.create(**validated_data)