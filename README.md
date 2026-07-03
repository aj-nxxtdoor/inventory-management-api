# Inventory Management API


A Flask REST API for managing retail inventory, with product lookups and imports from the OpenFoodFacts external API. Built as a summative lab for Moringa School.

## Features

- Full CRUD for inventory items (Create, Read, Update, Delete)
- External product lookup by barcode or name via the OpenFoodFacts API
- One-click import of external products directly into the inventory database
- CLI tool for interacting with the API from the terminal
- Automated test suite covering all endpoints

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy (SQLite database)
- Requests (for external API calls)
- Pytest (testing)

## Project Structure
inventory-management-api/
├── app/
│   ├── init.py       # Flask app factory + database setup
│   ├── models.py         # Item database model
│   ├── routes.py         # CRUD + external API routes
│   └── external_api.py   # OpenFoodFacts integration
├── cli/
│   └── cli.py             # Command-line interface
├── tests/
│   └── test_routes.py    # Pytest test suite
├── run.py                # App entry point
├── requirements.txt
└── README.md
## Setup

1. Clone the repo:
```bash
   git clone https://github.com/aj-nxxtdoor/inventory-management-api.git
   cd inventory-management-api
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Run the Flask server:
```bash
   python3 run.py
```

   The API will be running at `http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items` | Get all inventory items |
| GET | `/items/<id>` | Get a single item |
| POST | `/items` | Create a new item |
| PATCH | `/items/<id>` | Update an existing item |
| DELETE | `/items/<id>` | Delete an item |
| GET | `/external/barcode/<barcode>` | Look up a product by barcode (external API) |
| GET | `/external/search?name=<name>` | Search products by name (external API) |
| POST | `/items/import` | Import a product by barcode directly into inventory |

## Using the CLI

With the Flask server running in one terminal, open a second terminal and run:

```bash
python3 cli/cli.py
```

Follow the on-screen menu to list, add, update, delete, or import inventory items.

## Running Tests

```bash
python3 -m pytest tests/ -v
```

## Example Usage

Create an item:
```bash
curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d '{"name": "Coca-Cola 500ml", "quantity": 50, "price": 1.5}'
```

Import a product from OpenFoodFacts:
```bash
curl -X POST http://127.0.0.1:5000/items/import -H "Content-Type: application/json" -d '{"barcode": "3017620422003", "quantity": 20, "price": 4.99}'
```

## Author

ABDIFATAH BASHIR