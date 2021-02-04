import os


def create_key() -> str:
    key_generated = os.urandom(12)
    os.environ['JWT_SECRET_KEY'] = str(key_generated)

