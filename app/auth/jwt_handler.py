# This file is responsible for signing, encoding, decoding and returning JWTs
import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 600,
    }


def signJWT(email: str):
    payload = {
        "email": email,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}


def getEmailJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token['email']
    except:
        return None
