from flask import Blueprint, request, jsonify
from app.models.user import User
from extensions import db, bcrypt
from app.statuscodes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token
from datetime import datetime

# Define Blueprint
user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1')


# User Registration
@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        # Extract and validate fields
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        contact = data.get('contact')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')
        membership_status = data.get('membership_status')
        join_date = data.get('join_date')

        # Validate required fields
        if not first_name or not last_name or not email or not password:
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        # Validate email
        try:
            validate_email(email)
        except EmailNotValidError as e:
            return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), HTTP_409_CONFLICT

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            email=email,
            password=hashed_password,
            user_type=user_type,
            membership_status=membership_status,
            join_date=datetime.strptime(join_date, "%Y-%m-%d") if join_date else datetime.utcnow()
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
