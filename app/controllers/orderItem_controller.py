from flask import Blueprint, request, jsonify
from app.models.orderItem import OrderItem
from extensions import db
from app.statuscodes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

# Define Blueprint
order_item_bp = Blueprint('order_item_bp', __name__, url_prefix='/api/v1/orderitems')

# Create a new order item
@order_item_bp.route('/', methods=['POST'])
def create_order_item():
    try:
        data = request.get_json()
        
        order_id = data.get('order_id')
        merchandise_id = data.get('merchandise_id')
        quantity = data.get('quantity')
        price_of_item = data.get('price_of_item')

        if not (order_id and merchandise_id and quantity and price_of_item):
            return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

        new_order_item = OrderItem(
            order_id=order_id,
            merchandise_id=merchandise_id,
            quantity=quantity,
            price_of_item=price_of_item
        )

        db.session.add(new_order_item)
        db.session.commit()

        return jsonify({'message': 'Order item created successfully'}), HTTP_201_CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Retrieve an order item by ID
@order_item_bp.route('/<int:id>', methods=['GET'])
def get_order_item(id):
    try:
        order_item = OrderItem.query.get(id)
        if not order_item:
            return jsonify({'error': 'Order item not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': order_item.id,
            'order_id': order_item.order_id,
            'merchandise_id': order_item.merchandise_id,
            'quantity': order_item.quantity,
            'price_of_item': order_item.price_of_item,
            'total_amount': order_item.total_amount
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update an order item
@order_item_bp.route('/<int:id>', methods=['PUT'])
def update_order_item(id):
    try:
        order_item = OrderItem.query.get(id)
        if not order_item:
            return jsonify({'error': 'Order item not found'}), HTTP_404_NOT_FOUND

        data = request.get_json()
        
        order_item.order_id = data.get('order_id', order_item.order_id)
        order_item.merchandise_id = data.get('merchandise_id', order_item.merchandise_id)
        order_item.quantity = data.get('quantity', order_item.quantity)
        order_item.price_of_item = data.get('price_of_item', order_item.price_of_item)
        order_item.total_amount = order_item.quantity * order_item.price_of_item

        db.session.commit()

        return jsonify({'message': 'Order item updated successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete an order item
@order_item_bp.route('/<int:id>', methods=['DELETE'])
def delete_order_item(id):
    try:
        order_item = OrderItem.query.get(id)
        if not order_item:
            return jsonify({'error': 'Order item not found'}), HTTP_404_NOT_FOUND

        db.session.delete(order_item)
        db.session.commit()

        return jsonify({'message': 'Order item deleted successfully'}), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
