from uuid import uuid4


def generate_access_token() -> str:
    return str(uuid4())
