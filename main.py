from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"posts": [{"id": 1, "title": "Hello World"}]}


@app.post("/posts")
def create_post(new_post: Post):
    print(new_post)
    post_content = {
        "title": f"{new_post.title}",
        "content": f"{new_post.content}",
        "published": f"{new_post.published}",
        "rating": f"{new_post.rating}",
    }
    return {"post": post_content}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
