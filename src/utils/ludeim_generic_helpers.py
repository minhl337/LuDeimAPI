import hashlib


def generate_user_uuid(username: str, password_hash: str):
    return hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
