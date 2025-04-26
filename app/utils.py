from app.models import clients, programs, Client, Program

# Create a program
def create_program(program_name):
    if program_name not in programs:
        programs[program_name] = Program(program_name)
        return True
    return False

# Register a client
def register_client(client_id, name, age):
    if client_id not in clients:
        clients[client_id] = Client(client_id, name, age)
        return True
    return False

# Enroll a client in a program
def enroll_client(client_id, program_name):
    client = clients.get(client_id)
    if client and program_name in programs:
        if program_name not in client.enrolled_programs:
            client.enrolled_programs.append(program_name)
            return True
    return False

# Find a client by ID
def find_client(client_id):
    return clients.get(client_id)
