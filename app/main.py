from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post,user,auth

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    try:
         conn = psycopg2.connect(host='localhost',   database='practice_fastapi', user='postgres', password='samia16', 
         cursor_factory=RealDictCursor)
         cursor = conn.cursor()
         print("Databasee connection was successful")
         break
    except Exception as error:
         print("Connection to database failed")
         print("Error: ", error)
         time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favourite foods", "content": "i like pizza", "id": 2}]



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        

def find_index_post(id):
    for i, p in enumerate (my_posts):
        if p['id'] == id:
            return i
        

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def health():
    return {"message": "hello samia"}



@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return{"new_post" : f"title {payLoad['title']} content: {payLoad['content']}"}


    #return{'message': "updated post"} 







