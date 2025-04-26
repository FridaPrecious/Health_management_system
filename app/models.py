clients = {}
programs = {}

class Client:
    def __init__(self, client_id, name, age):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.enrolled_programs = []

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "name": self.name,
            "age": self.age,
            "enrolled_programs": self.enrolled_programs
        }

class Program:
    def __init__(self, name):
        self.name = name
