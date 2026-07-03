import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "InventoryManagementApp/1.0 (student project - Moringa School)"
}

def search_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get('status') != 1:
        return None

    product = data.get('product', {})
    return {
        'name': product.get('product_name', 'Unknown'),
        'barcode': barcode,
        'category': product.get('categories', 'Unknown'),
        'price': None,
        'quantity': 0
    }

def search_by_name(name):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        'search_terms': name,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 5
    }
    response = requests.get(url, params=params, headers=HEADERS)

    if response.status_code != 200:
        return []

    data = response.json()
    products = data.get('products', [])

    results = []
    for product in products:
        results.append({
            'name': product.get('product_name', 'Unknown'),
            'barcode': product.get('code', ''),
            'category': product.get('categories', 'Unknown'),
            'price': None,
            'quantity': 0
        })

    return results