from flask import Blueprint, request, jsonify
from app.models.order import Order
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
order_bp = Blueprint('order_bp', __name__, url_prefix='/api/v1/orders')

# Create a new order
@order_bp.route('/', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        status_of_order = data.get('status_of_order')
        address_of_delivery = data.get('address_of_delivery')
        order_date = data.get('order_date')

        if not (user_id and status_of_order and address_of_delivery):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_order = Order(
            user_id=user_id,
            status_of_order=status_of_order,
            address_of_delivery=address_of_delivery,
            order_date=datetime.strptime(order_date, "%Y-%m-%d") if order_date else datetime.utcnow()
        )

        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Order created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve an order by ID
@order_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({'error': 'Order not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': order.id,
            'user_id': order.user_id,
            'order_date': order.order_date,
            'status_of_order': order.status_of_order,
            'address_of_delivery': order.address_of_delivery,
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update an order
@order_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({'error': 'Order not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()
        
        order.user_id = data.get('user_id', order.user_id)
        order.status_of_order = data.get('status_of_order', order.status_of_order)
        order.address_of_delivery = data.get('address_of_delivery', order.address_of_delivery)
        order.order_date = datetime.strptime(data.get('order_date'), "%Y-%m-%d") if data.get('order_date') else order.order_date

        db.session.commit()

        return jsonify({'message': 'Order updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete an order
@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({'error': 'Order not found'}), HTTP_404_NOT_FOUND

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
