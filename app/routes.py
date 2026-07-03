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