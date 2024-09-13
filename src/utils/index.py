import secrets
import string
import hashlib
from urllib.parse import urlparse


def generate_secret_key(length=20):
    # Generate a random string of `length` characters
    # Since each byte results in 2 hex characters, we need `length // 2` bytes
    # Adjusting for odd lengths to ensure the final string meets the required length
    bytes_length = (length + 1) // 2  # Adjust for odd lengths
    secret_key = secrets.token_hex(bytes_length)[:length]  # Ensure the key is exactly `length` characters
    return secret_key


def generate_index_name(base, table):
    characters = string.ascii_lowercase

    # Generate a random string of 5 characters from the defined set
    # We use 5 because one character is reserved for the underscore prefix
    random_part = ''.join(secrets.choice(characters) for i in range(5))

    new_name = f"{base}_{table}_{random_part}_index"
    return new_name


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def parse_postgres_url(url: str) -> dict:
    """
    Parse a PostgreSQL URL and extract specific components.

    :param url: PostgreSQL URL string
    :return: Dictionary containing extracted components
    """
    parsed = urlparse(url)

    # Extract components
    username = parsed.username or ""
    password = parsed.password or ""
    hostname = parsed.hostname or ""
    port = str(parsed.port) if parsed.port else ""

    # Construct the result dictionary
    result = {
        "PG_USER": username,
        "PG_HOST": hostname,
        "PG_PORT": port,
        "PG_PASSWORD": password
    }

    return result
