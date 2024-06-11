from flask import Blueprint, request, jsonify
from app.models.contact import Contact
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
contact_bp = Blueprint('contact_bp', __name__, url_prefix='/api/v1/contacts')

# Create a new contact
@contact_bp.route('/', methods=['POST'])
def create_contact():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not (name and email and message):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_contact = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_contact)
        db.session.commit()

        return jsonify({'message': 'Contact created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve all contacts
@contact_bp.route('/', methods=['GET'])
def get_all_contacts():
    try:
        contacts = Contact.query.all()
        result = [
            {
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'message': contact.message,
                'date': contact.date
            } for contact in contacts
        ]
        return jsonify(result), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve a single contact by ID
@contact_bp.route('/<int:id>', methods=['GET'])
def get_contact(id):
    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'message': contact.message,
            'date': contact.date
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update a contact
@contact_bp.route('/<int:id>', methods=['PUT'])
def update_contact(id):
    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()

        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.message = data.get('message', contact.message)
        contact.date = datetime.strptime(data.get('date'), "%Y-%m-%d %H:%M:%S") if data.get('date') else contact.date

        db.session.commit()

        return jsonify({'message': 'Contact updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete a contact
@contact_bp.route('/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({'error': 'Contact not found'}), HTTP_404_NOT_FOUND

        db.session.delete(contact)
        db.session.commit()

        return jsonify({'message': 'Contact deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
