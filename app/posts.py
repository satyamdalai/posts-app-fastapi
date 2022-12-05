from fastapi import APIRouter, Request, Depends, HTTPException, Body, status
from fastapi.encoders import jsonable_encoder
from app.model import PostSchema, PostFormSchema, PostUpdateSchema
from app.auth.jwt_handler import getEmailJWT
from app.auth.jwt_bearer import jwtBearer
from typing import List

router = APIRouter()


@router.get("/", response_model=List[PostSchema])
def get_posts(request: Request):
    all_posts = list(request.app.posts.find())
    return all_posts


@router.get("/{id}", response_model=PostSchema)
def get_one_post(id: str, request: Request):
    if (post := request.app.posts.find_one({"_id": id})) is not None:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with ID {id} not found")


@router.get("/byUser/", response_model=List[PostSchema], dependencies=[Depends(jwtBearer())])
def get_user_posts(request: Request, session_token: str = Depends(jwtBearer())):
    email = getEmailJWT(session_token)
    if email is not None:
        user_posts = list(request.app.posts.find({"userEmail": email}))
        return user_posts
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid or Expired Token!")


@router.post("/", response_model=PostSchema, dependencies=[Depends(jwtBearer())])
def add_post(post: PostFormSchema, request: Request, session_token: str = Depends(jwtBearer())):
    post = jsonable_encoder(post)
    email = getEmailJWT(session_token)
    if email is not None:
        post["userEmail"] = email
        new_post = request.app.posts.insert_one(post)
        created_post = request.app.posts.find_one(
            {"_id": new_post.inserted_id}
        )
        return created_post
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid or Expired Token!")


@router.put("/{id}", response_model=PostSchema, dependencies=[Depends(jwtBearer())])
def update_post(id: str, request: Request, post: PostUpdateSchema = Body(default=None)):
    post = jsonable_encoder(post)
    update_result = request.app.posts.update_one(
        {"_id": id}, {"$set": post})
    if update_result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")

    if (
        existing_post := request.app.posts.find_one({"_id": id})
    ) is not None:
        return existing_post
