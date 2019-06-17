import hashlib


def generate_user_user_id(username: str, password_hash: str):
    return hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
