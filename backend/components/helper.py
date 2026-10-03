from pwdlib import PasswordHash

passwordHash = PasswordHash.recommended()

def hash_password(raw_password):
    return passwordHash.hash(raw_password)

def verify_password(raw_password, hashed):
    return passwordHash.verify(raw_password, hashed)
