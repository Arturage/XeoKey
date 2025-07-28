from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory storage for services
services = []

# Helper to find service by id

def find_service(service_id):
    for srv in services:
        if srv['id'] == service_id:
            return srv
    return None

@app.route('/services', methods=['GET'])
def get_services():
    return jsonify(services)

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    srv = find_service(service_id)
    if not srv:
        abort(404)
    return jsonify(srv)

@app.route('/services', methods=['POST'])
def create_service():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description='Service name required')
    service_id = services[-1]['id'] + 1 if services else 1
    service = {'id': service_id, 'name': data['name'], 'description': data.get('description', '')}
    services.append(service)
    return jsonify(service), 201

@app.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    srv = find_service(service_id)
    if not srv:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400)
    srv['name'] = data.get('name', srv['name'])
    srv['description'] = data.get('description', srv['description'])
    return jsonify(srv)

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    srv = find_service(service_id)
    if not srv:
        abort(404)
    services.remove(srv)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
