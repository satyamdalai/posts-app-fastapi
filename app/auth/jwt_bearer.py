# The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decodeJWT


class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Token Type Invalid!")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid or Expired Token!")
            session_token = credentials.credentials
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid or Expired Token!")

    def verify_jwt(self, jwttoken: str):
        isTokenValid: bool = False  # A false flag
        payload = decodeJWT(jwttoken)
        if payload:
            isTokenValid = True
        return isTokenValid
