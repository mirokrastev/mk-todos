from django.contrib.auth.hashers import make_password


def generate_identifier(to_hash):
    hashed_identifier = make_password(to_hash)[-20:-5]
    return hashed_identifier
