from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class PostSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userEmail: str = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "post_demo": {
                "userEmail": "User email",
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }


class PostFormSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "post_demo": {
                "userEmail": "User email",
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }


class PostUpdateSchema(BaseModel):
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        schema_extra = {
            "post_demo": {
                "userEmail": "User email",
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }


class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(default=None)
    name: str = Field(default=None)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        the_schema = {
            "user_demo": {
                "email": "raj@example.com",
                "name": "Raj"
            }
        }


class UserSignUpSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(default=None)
    name: str = Field(default=None)
    password: str = Field(default=None)

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        the_schema = {
            "user_demo": {
                "email": "raj@example.com",
                "name": "Raj",
                "password": "123"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "email": "raj@example.com",
                "password": "123"
            }
        }
