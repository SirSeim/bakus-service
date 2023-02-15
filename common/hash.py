import hashlib
import uuid


def hash_id(string: str) -> uuid.UUID:
    return uuid.UUID(hashlib.blake2b(str.encode(string), digest_size=16).hexdigest())
