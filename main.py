import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = uuid.uuid4().hex
    posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: str):
    print(id)
    for post in posts:
        if post["id"] == id:
            return {"data": post}

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
    )


@app.delete("/posts/{id}")
def delete_post(id: str):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exist",
    )
