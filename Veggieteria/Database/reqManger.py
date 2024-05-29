from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store
data_store = []

# Route for GET request
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data_store), 200

# Route for POST request
@app.route('/items', methods=['POST'])
def add_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"error": "Invalid data"}), 400
    item = {
        'id': len(data_store) + 1,
        'name': request.json['name']
    }
    data_store.append(item)
    return jsonify(item), 201

# Route for PUT request
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data_store if item['id'] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    if not request.json or not 'name' in request.json:
        return jsonify({"error": "Invalid data"}), 400
    item['name'] = request.json['name']
    return jsonify(item), 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)
