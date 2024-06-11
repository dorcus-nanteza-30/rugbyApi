from flask import Blueprint, request, jsonify
from app.models.merchanise import Merchandise
from extensions import db
from app.statuscodes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# Define Blueprint
merchandise_bp = Blueprint('merchandise_bp', __name__, url_prefix='/api/v1/merchandises')

# Create a new merchandise item
@merchandise_bp.route('/', methods=['POST'])
def create_merchandise():
    try:
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        image = data.get('image')
        category = data.get('category')

        if not (name and description and price and stock and image and category):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_merchandise = Merchandise(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image,
            category=category
        )

        db.session.add(new_merchandise)
        db.session.commit()

        return jsonify({'message': 'Merchandise created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve a merchandise item by ID
@merchandise_bp.route('/<int:id>', methods=['GET'])
def get_merchandise(id):
    try:
        merchandise = Merchandise.query.get(id)
        if not merchandise:
            return jsonify({'error': 'Merchandise not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': merchandise.id,
            'name': merchandise.name,
            'description': merchandise.description,
            'price': merchandise.price,
            'stock': merchandise.stock,
            'image': merchandise.image,
            'category': merchandise.category
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update a merchandise item
@merchandise_bp.route('/<int:id>', methods=['PUT'])
def update_merchandise(id):
    try:
        merchandise = Merchandise.query.get(id)
        if not merchandise:
            return jsonify({'error': 'Merchandise not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()
        
        merchandise.name = data.get('name', merchandise.name)
        merchandise.description = data.get('description', merchandise.description)
        merchandise.price = data.get('price', merchandise.price)
        merchandise.stock = data.get('stock', merchandise.stock)
        merchandise.image = data.get('image', merchandise.image)
        merchandise.category = data.get('category', merchandise.category)

        db.session.commit()

        return jsonify({'message': 'Merchandise updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete a merchandise item
@merchandise_bp.route('/<int:id>', methods=['DELETE'])
def delete_merchandise(id):
    try:
        merchandise = Merchandise.query.get(id)
        if not merchandise:
            return jsonify({'error': 'Merchandise not found'}), HTTP_404_NOT_FOUND

        db.session.delete(merchandise)
        db.session.commit()

        return jsonify({'message': 'Merchandise deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
