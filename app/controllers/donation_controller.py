from flask import Blueprint, request, jsonify
from app.models.donation import Donation
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
donation_bp = Blueprint('donation_bp', __name__, url_prefix='/api/v1/donations')

# Create a new donation
@donation_bp.route('/', methods=['POST'])
def create_donation():
    try:
        data = request.get_json()

        user_id = data.get('user_id')
        amount = data.get('amount')
        donation_date = data.get('donation_date')
        message = data.get('message')

        if not (user_id and amount):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_donation = Donation(
            user_id=user_id,
            amount=amount,
            donation_date=datetime.strptime(donation_date, "%Y-%m-%d %H:%M:%S") if donation_date else None,
            message=message
        )

        db.session.add(new_donation)
        db.session.commit()

        return jsonify({'message': 'Donation created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve a donation by ID
@donation_bp.route('/<int:id>', methods=['GET'])
def get_donation(id):
    try:
        donation = Donation.query.get(id)
        if not donation:
            return jsonify({'error': 'Donation not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': donation.id,
            'user_id': donation.user_id,
            'amount': donation.amount,
            'donation_date': donation.donation_date,
            'message': donation.message
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update a donation
@donation_bp.route('/<int:id>', methods=['PUT'])
def update_donation(id):
    try:
        donation = Donation.query.get(id)
        if not donation:
            return jsonify({'error': 'Donation not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()

        donation.amount = data.get('amount', donation.amount)
        donation.donation_date = datetime.strptime(data.get('donation_date'), "%Y-%m-%d %H:%M:%S") if data.get('donation_date') else donation.donation_date
        donation.message = data.get('message', donation.message)

        db.session.commit()

        return jsonify({'message': 'Donation updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete a donation
@donation_bp.route('/<int:id>', methods=['DELETE'])
def delete_donation(id):
    try:
        donation = Donation.query.get(id)
        if not donation:
            return jsonify({'error': 'Donation not found'}), HTTP_404_NOT_FOUND

        db.session.delete(donation)
        db.session.commit()

        return jsonify({'message': 'Donation deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
