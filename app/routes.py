from flask import Blueprint, jsonify, request
from app import db
from app.models import Item
main = Blueprint('main', __name__)
@main.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200
@main.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict()), 200
@main.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    new_item = Item(
        name=data.get('name'),
        barcode=data.get('barcode'),
        category=data.get('category'),
        quantity=data.get('quantity', 0),
        price=data.get('price')
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201
@main.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    data = request.get_json()

    if 'name' in data:
        item.name = data['name']
    if 'barcode' in data:
        item.barcode = data['barcode']
    if 'category' in data:
        item.category = data['category']
    if 'quantity' in data:
        item.quantity = data['quantity']
    if 'price' in data:
        item.price = data['price']

    db.session.commit()
    return jsonify(item.to_dict()), 200