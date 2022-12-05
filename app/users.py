from fastapi import APIRouter, Request, HTTPException, Body, status
from fastapi.encoders import jsonable_encoder
from app.model import UserSchema, UserLoginSchema, UserSignUpSchema
from app.auth.jwt_handler import signJWT
from passlib.hash import bcrypt

router = APIRouter()


@router.post("/signup", response_model=UserSchema)
def user_signup(request: Request, user: UserSignUpSchema = Body(default=None)):
    user = jsonable_encoder(user)
    u_email = user["email"]
    if (request.app.users.find_one({"email": u_email})) is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the {u_email} already present!")
    user["password"] = bcrypt.hash(user["password"])
    new_user = request.app.users.insert_one(user)
    created_user = request.app.users.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


def authenticate_user(request: Request, data: UserLoginSchema):
    for user in request.app.users.find():
        if user['email'] == data.email and bcrypt.verify(data.password, user['password']):
            return True
    return False


@router.post("/login")
def user_login(request: Request, user: UserLoginSchema = Body(default=None)):

    if authenticate_user(request, user):
        token = signJWT(user.email)
        return token
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Ivalid Credentials")
