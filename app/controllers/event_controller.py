from flask import Blueprint, request, jsonify
from app.models.event import Event
from extensions import db
from app.statuscodes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from datetime import datetime

# Define Blueprint
event_bp = Blueprint('event_bp', __name__, url_prefix='/api/v1/events')

# Create a new event
@event_bp.route('/', methods=['POST'])
def create_event():
    try:
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        date = data.get('date')
        location = data.get('location')

        if not (name and description and date and location):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_event = Event(
            name=name,
            description=description,
            date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
            location=location
        )

        db.session.add(new_event)
        db.session.commit()

        return jsonify({'message': 'Event created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve an event by ID
@event_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    try:
        event = Event.query.get(id)
        if not event:
            return jsonify({'error': 'Event not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date,
            'location': event.location
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update an event
@event_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    try:
        event = Event.query.get(id)
        if not event:
            return jsonify({'error': 'Event not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()

        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.date = datetime.strptime(data.get('date'), "%Y-%m-%d %H:%M:%S") if data.get('date') else event.date
        event.location = data.get('location', event.location)

        db.session.commit()

        return jsonify({'message': 'Event updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete an event
@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event = Event.query.get(id)
        if not event:
            return jsonify({'error': 'Event not found'}), HTTP_404_NOT_FOUND

        db.session.delete(event)
        db.session.commit()

        return jsonify({'message': 'Event deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
