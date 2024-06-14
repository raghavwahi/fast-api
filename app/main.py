from typing import Optional

import psycopg
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
from pydantic import BaseModel

from app.util.config import settings

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    conn = psycopg.connect(
        f"dbname={settings.PG_DATABASE} user={settings.PG_USER} password={settings.PG_PASSWORD} host={settings.PG_HOST} port={settings.PG_PORT}",
        row_factory=dict_row,
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {settings.PG_SCHEMA}.posts")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(posts) + 1
    posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    for post in posts:
        if post["id"] == id:
            return {"data": post}

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {id} not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
    )


@app.delete("/posts/{id}")
def delete_post(id: int):
    for index, post in enumerate(posts):
        if post["id"] == id:
            posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exist",
    )


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    for index, post_data in enumerate(posts):
        if post_data["id"] == id:
            post_dict = post.dict()
            post_dict["id"] = id
            posts[index] = post_dict
            return {"data": post_dict}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exist",
    )
