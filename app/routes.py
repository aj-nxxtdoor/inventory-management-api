from flask import Blueprint, jsonify, request
from app import db
from app.models import Item
from app.external_api import search_by_barcode, search_by_name

main = Blueprint('main', __name__)

# GET all items
@main.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# GET a single item by id
@main.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict()), 200

# CREATE a new item
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

# UPDATE (patch) an existing item
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

# DELETE an item
@main.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item {item_id} deleted'}), 200

# Search external API by barcode (just returns the data, doesn't save it)
@main.route('/external/barcode/<barcode>', methods=['GET'])
def lookup_barcode(barcode):
    result = search_by_barcode(barcode)
    if not result:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(result), 200

# Search external API by name (just returns the data, doesn't save it)
@main.route('/external/search', methods=['GET'])
def lookup_name():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Please provide a name query param'}), 400
    results = search_by_name(name)
    return jsonify(results), 200

# Import a product from external API straight into the inventory database
@main.route('/items/import', methods=['POST'])
def import_item():
    data = request.get_json()
    barcode = data.get('barcode')

    if not barcode:
        return jsonify({'error': 'Barcode is required'}), 400

    product = search_by_barcode(barcode)
    if not product:
        return jsonify({'error': 'Product not found in external API'}), 404

    new_item = Item(
        name=product['name'],
        barcode=product['barcode'],
        category=product['category'],
        quantity=data.get('quantity', 0),
        price=data.get('price')
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201