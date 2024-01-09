from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "id": 1,
        "title": "Introduction to python",
        "content": "This is the best introductory article to learning python"
    },

    {
        "id": 2,
        "title": "Introduction to Java",
        "content": "This is the best introductory article to learning Java"
    },
    {
        "id": 3,
        "title": "Introduction to C++",
        "content": "This is the best introductory article to learning C++"
    }
]

def find_post_index(id):
    """Returns the index of post based on it's ID"""
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

def calculate_post_id():
    """Calculate the id of a newly created post"""
    post_len = len(my_posts)
    return post_len + 1


@app.get("/check", status_code=status.HTTP_200_OK)
def index():
    """Checks the heath of the API, if ok, returns OK"""
    return {"message": "OK"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"posts": my_posts}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post_detail(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with given id not found")
    post = my_posts[index]
    return {"data": post}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = calculate_post_id()
    # append post to the list of posts
    my_posts.append(post_dict)
    return {"post": post_dict}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # get the index of a post
    index = find_post_index(id)
    if index is None:
        # update the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with given id not found")

    new_post = post.model_dump()
    new_post["id"] = id
    my_posts[index] = new_post
    return {"data": my_posts[index]}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # get index of post in the lst
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")
    # remove post from the list
    print("This is the index", index)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
