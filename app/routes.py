from flask import Blueprint, render_template, request, jsonify
from app.models import Program, Client, clients, programs
from app.utils import create_program, register_client, enroll_client, find_client

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/programs', methods=['POST'])
def create_program_route():
    program_name = request.json.get('programName')
    if program_name and create_program(program_name):
        return jsonify({
            'message': 'Program created successfully.',
            'program': program_name
        })
    return jsonify({'message': 'Program already exists or invalid input.'}), 400

@main.route('/clients', methods=['POST'])
def register_client_route():
    client_id = request.json.get('clientId')
    name = request.json.get('name')
    age = request.json.get('age')

    if client_id and name and age and register_client(client_id, name, age):
        return jsonify({
            'message': 'Client registered successfully.',
            'client': {
                'id': client_id,
                'name': name,
                'age': age
            }
        })
    return jsonify({'message': 'Client already exists or invalid input.'}), 400

@main.route('/clients/enroll', methods=['POST'])
def enroll_client_route():
    client_id = request.json.get('clientId')
    program_name = request.json.get('programName')

    if enroll_client(client_id, program_name):
        client = clients.get(client_id)
        return jsonify({
            'message': f'{client_id} enrolled in {program_name} successfully.',
            'client': client.to_dict()
        })
    return jsonify({'message': 'Client or Program not found.'}), 400

@main.route('/clients/<client_id>', methods=['GET'])
def view_client(client_id):
    client = find_client(client_id)
    if client:
        return jsonify(client.to_dict())
    return jsonify({'message': 'Client not found.'}), 404

@main.route('/clients/delete/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    if client_id in clients:
        del clients[client_id]
        return jsonify({'message': f'Client {client_id} deleted successfully.'})
    return jsonify({'message': 'Client not found.'}), 404

@main.route('/clients/remove_from_program', methods=['POST'])
def remove_from_program():
    client_id = request.json.get('clientId')
    program_name = request.json.get('programName')

    client = clients.get(client_id)
    if client and program_name in client.enrolled_programs:
        client.enrolled_programs.remove(program_name)
        return jsonify({
            'message': f'{client_id} removed from {program_name} successfully.',
            'client': client.to_dict()
        })
    return jsonify({'message': 'Client not enrolled in this program.'}), 400

@main.route('/clients/list', methods=['GET'])
def list_clients():
    client_list = [client.to_dict() for client in clients.values()]
    return jsonify({'clients': client_list})

@main.route('/programs/list', methods=['GET'])
def list_programs():
    program_list = [program.name for program in programs.values()]
    return jsonify({'programs': program_list})
