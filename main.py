import uuid

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


posts = []

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = uuid.uuid4().hex
    posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: str, response: Response):
    print(id)
    for post in posts:
        if post["id"] == id:
            return {"data": post}

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
