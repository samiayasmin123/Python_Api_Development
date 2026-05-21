from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db  



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    

)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id:int=
Depends(oauth2.get_current_user)):
    #cursor.execute("""select * from posts""")
    #posts = cursor.fetchall()
    posts =  db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int=
Depends(oauth2.get_current_user)):
    
    #cursor.execute("""insert into posts(title, content, published) values (%s, %s, %s) returning
                  # * """,(post.title, post.content, post.published ))
    
    #new_post = cursor.fetchone()
   # conn.commit()
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db:Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    #cursor.execute("""select * from posts where id = %s """, (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id: int, db:Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):

    #cursor.execute(""" delete from posts where id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
    
    
    
    #return{'message': 'post was successfully deleted'}
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)):
    
    #cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s
    #returning *""",
    #               (post.title, post.content, post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} does not exist")
    

    
    
    post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    
    db.commit()

    #return{"data": 'successful'}
    return post_query.first()