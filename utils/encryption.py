import hashlib

salt = "natahiko"


def get_hash(str):
    str = hashlib.md5(str.encode())
    res1 = str.hexdigest() + salt
    str = hashlib.md5(res1.encode())
    return str.hexdigest()
