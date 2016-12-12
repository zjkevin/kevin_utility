import hashlib


def md5(hash_str):
    __m = hashlib.md5()
    __m.update(bytes(hash_str, encoding="utf8"))
    return __m.hexdigest()
