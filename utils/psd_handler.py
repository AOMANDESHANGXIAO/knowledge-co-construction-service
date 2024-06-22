from passlib.handlers.sha2_crypt import sha256_crypt


def hash_password(password: str):
    """密码加密"""
    return sha256_crypt.encrypt(password)


def verify_password(password: str, db_password: str):
    """校验密码"""
    return sha256_crypt.verify(password, db_password)