from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="miclem", password="1234", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE CONNECTION WAS SUCCESSFUL")
        break
    except psycopg2.Error as e:
        print("Could not establish a connection to the database")
        print(e)
        time.sleep(3)




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    created_at: str


@app.get("/check", status_code=status.HTTP_200_OK)
def index():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    sql_statemtent = """SELECT * FROM posts;"""
    cursor.execute(sql_statemtent)
    posts = cursor.fetchall()
    return {"posts": posts}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int):
    sql_statement = """SELECT * FROM posts WHERE id = (%s)"""
    sql_params = (id,)
    cursor.execute(sql_statement, sql_params)
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    # prepare the statement
   
    sql_statemtent = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """
    insert_params = (post.title, post.content, post.published)
    cursor.execute(sql_statemtent, insert_params)
    post = cursor.fetchone()
    conn.commit()
    return {"post": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    sql_statement = """UPDATE posts SET title = %s, content = %s, published = %s, created_at = %s WHERE id = %s RETURNING *;"""
    sql_params = (post.title, post.content, post.published, post.created_at, id)
    cursor.execute(sql_statement, sql_params)
    post = cursor.fetchone()
    if post is None:
        # update the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with given id not found")
    conn.commit()
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    sql_statement = """DELETE FROM posts WHERE id = %s RETURNING *;"""
    sql_params = (id,)
    cursor.execute(sql_statement, sql_params)
    post = cursor.fetchone()
    print(post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
