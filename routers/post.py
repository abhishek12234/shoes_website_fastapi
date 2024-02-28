from fastapi import FastAPI,Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2

from typing import List, Optional
import base64




router=APIRouter()
@router.get("/get_post/{id}",response_model=schemas.Shoes)
def test_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #posts=db.execute(text("SELECT * FROM POSTS WHERE id=:id"),{"id":id})
    posts=db.query(models.Shoes).filter(models.Shoes.id==id).first()
    if posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    return posts

@router.get("/delete_shoes/{id}")
def read(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    
    post_query=db.query(models.Shoes).filter(models.Shoes.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted"}

@router.get("/shoes", response_model=List[schemas.Shoes])
def read(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
     
     
    shoes_list = db.query(models.Shoes).all()

   
    # Prepare a dictionary with all the required fields
    
    

    return shoes_list
@router.get("/featured_shoes", response_model=List[schemas.Shoes])
def read(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
     
     
    shoes_list = db.query(models.Shoes).filter(models.Shoes.shoes_type=="Featured").all()

   
    # Prepare a dictionary with all the required fields
    
    

    return shoes_list

@router.post("/createshoes")
async def create_post(post:schemas.ShoesCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
    decoded_image = base64.b64decode(post.product_image)
    new_shoes=models.Shoes(name=post.name,price=post.price,product_image=decoded_image,shoes_type=post.shoes_type,shoes_category=post.shoes_category)
    db.add(new_shoes)
    db.commit()
    
   
    return {"id":new_shoes.id}
@router.put("/updateshoes/{id}")
def update_shoes(id:int,post:schemas.ShoesCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    shoes_query=db.query(models.Shoes).filter(models.Shoes.id==id)
    shoes=shoes_query.first()
    if shoes==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    shoes_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data":"sucess"}