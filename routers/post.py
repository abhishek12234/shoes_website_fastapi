from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,UploadFile,File
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2
from config import settings
from typing import List, Optional
import base64

import boto3
AWS_ACCESS_KEY = "AKIAVRUVPPBZ74UNU3OZ"  # Replace with the actual Access Key ID
  # Replace with the actual Secret Access Key
AWS_REGION = "ap-south-1"
S3_BUCKET_NAME = "abhishek-jain-786"

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=settings.aws_secret_key, region_name=AWS_REGION)

router=APIRouter()
s3_bucket_name="abhishek-jain-786"

@router.post("/add_shoes_image",response_model=schemas.Shoes)
def add_shoes_image(file:UploadFile,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #posts=db.execute(text("SELECT * FROM POSTS WHERE id=:id"),{"id":id})
    posts=db.query(models.Shoes).filter(models.Shoes.id==id).first()
    if posts==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    return posts

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

@router.post("/createshoesimagelink")
async def create_post(file:UploadFile=File(...), db: Session = Depends(get_db)):
   
    
    
    s3.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)

        # Generate the URL of the uploaded file
    file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
    
    print(file_url)
    
    return file_url
@router.post("/createshoes")
async def create_shoes(shoes:schemas.ShoesCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_shoes=models.Shoes(**shoes.dict())

    db.add(new_shoes)
    
    db.commit()
    db.refresh(new_shoes)
    return new_shoes
  


@router.put("/updateshoes/{id}")
def update_shoes(id:int,post:schemas.ShoesCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    shoes_query=db.query(models.Shoes).filter(models.Shoes.id==id)
    shoes=shoes_query.first()
    if shoes==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    shoes_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {"data":"sucess"}