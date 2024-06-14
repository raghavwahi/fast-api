from typing import Optional

import psycopg
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
from pydantic import BaseModel

from app.util.config import settings

app = FastAPI()

conn = psycopg.connect(
    f"dbname={settings.PG_DATABASE} user={settings.PG_USER} password={settings.PG_PASSWORD} host={settings.PG_HOST} port={settings.PG_PORT}",
    row_factory=dict_row,
)
cur = conn.cursor()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello world from Fast API"}


@app.get("/posts")
def get_posts():
    cur.execute(f"SELECT * FROM {settings.PG_SCHEMA}.posts")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute(
        f"INSERT INTO {settings.PG_SCHEMA}.posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.publish),
    )
    conn.commit()
    new_post = cur.fetchone()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: str):
    cur.execute(f"SELECT * FROM {settings.PG_SCHEMA}.posts WHERE id = %s", (id,))
    post = cur.fetchone()
    if post:
        return {"data": post}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
    )


@app.delete("/posts/{id}")
def delete_post(id: str):
    cur.execute(
        f"DELETE FROM {settings.PG_SCHEMA}.posts WHERE id = %s RETURNING *", (id,)
    )
    conn.commit()
    deleted_post = cur.fetchone()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exist",
    )


@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    cur.execute(
        f"UPDATE {settings.PG_SCHEMA}.posts SET title= %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.publish, id),
    )
    conn.commit()
    updated_post = cur.fetchone()
    if updated_post:
        return {"data": updated_post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} does not exist",
    )
