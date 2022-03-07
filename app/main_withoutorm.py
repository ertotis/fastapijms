from ast import Dict
from msilib.schema import Error
from typing import Optional
from fastapi import Body, FastAPI,Response, status,HTTPException
from pydantic import BaseModel, PositiveInt
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time




app=FastAPI()
#We create a class that is the template for our posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #if user doesn't provide published the default is tru
    


my_posts=[  {"title":"title of post 1", "content": "content of post 1", "id": 1},
            {"title":"favorite foods", "content": "I like pizza", "id": 2}]

#Creating a cursor to join our database
while True:

    try:
        conn = psycopg.connect( host='localhost', dbname='fastapi', user='postgres', password='password123',
                                )
        #the information will be received in dict like language (useful for json)
        cursor=conn.cursor(row_factory=dict_row)
        print("Database connection established")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)



def find_post(id):
    for p in my_posts:
        
        if p["id"] == id:
            return p

#use of the enumerate class that basically counts up until you reach your value
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']== id:
            return i

@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()

    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(payLoad: dict=Body(...)):
def create_posts(post: Post): 
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",
                    ( post.title, post.content, post.published))
    new_post=cursor.fetchone()

    conn.commit()
    return {"data": new_post}
#title str, content str


@app.get("/posts/{id}") #id is a path parameter
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post=cursor.fetchone()
    if not post:
        # one way to do it:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post=cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} does not exist")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")  
def update_post(id:int ,post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
                    WHERE id=%s RETURNING *""", (post.title, post.content, post.published,
                    str(id)))   
    updated_post=cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} does not exist")
    
    conn.commit()
    return {"data" : updated_post}