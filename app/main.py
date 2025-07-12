from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import time
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn=psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="messi10", cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("database connection successful")
    
except Exception as e:
    print("connection failed. error: ",e)
    time.sleep(5)

class Post(BaseModel):
    title:str
    content:str
    post:bool = True
    rating:Optional[int] = None

app = FastAPI()

@app.get("/")
def get_msg():
    return {"message": "this is my first api"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from socialmedia_app""")
    my_posts=cursor.fetchall()
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_data(post:Post):
    cursor.execute("""insert into socialmedia_app (title,content,rating,post) values (%s,%s,%s,%s) returning *""",(post.title,post.content,post.rating,post.post))
    new_post=cursor.fetchone()
    conn.commit()
    return {"description":"posts page",
            "data": new_post
            }

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(f"""select * from socialmedia_app where id={id}""")
    my_post=cursor.fetchone()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    return{"post_detail": my_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int):
    cursor.execute(f"""delete from socialmedia_app where id={id} returning *""")
    my_post=cursor.fetchone()
    if my_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    conn.commit()

@app.put("/posts/{id}")
def update_post(id:int, update:Post):
    cursor.execute("""update socialmedia_app set title=(%s),content=(%s),rating=(%s),post=(%s) where id=%s returning *""",(update.title,update.content,update.rating,update.post,id))
    my_post=cursor.fetchone()
    if my_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no such post with id={id} exists")
    conn.commit()
    return {"message":f"your post with id {id} has been updated",
            "data":my_post
            }

