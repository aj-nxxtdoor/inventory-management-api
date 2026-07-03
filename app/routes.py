from flask import Blueprint, jsonify, request
from app import db
from app.models import Item
main = Blueprint('main', __name__)
@main.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200