from fastapi import FastAPI,Depends,HTTPException,APIRouter,status
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2
from sqlalchemy.exc import IntegrityError

from typing import List, Optional

router=APIRouter()


@router.post("/add_item_cart",response_model=schemas.CartOut)
def add_item_cart(shoes_id:schemas.CartAdd,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    id=dict(current_user["token_data"])["id"]
    print(current_user["token_data"])
    user_email=db.query(models.User).filter(models.User.id==id).first()
    shoes=db.query(models.Shoes).filter(models.Shoes.id==shoes_id.id).first()
    print(user_email.email)
    cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email).all()
    new_item=models.Cart(product_id=shoes.id,owner_email=user_email.email,owner_id=id,product_image=shoes.product_image,price=shoes.price,product_name=shoes.name, shoes_category=shoes.shoes_category)

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except IntegrityError as e:
        db.rollback()
        
        raise HTTPException(status_code=400, detail="Unique constraint violation: Item already exists")
   
@router.get("/all_cart_items",response_model=List[schemas.CartOut])
def add_item_cart(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    id=dict(current_user["token_data"])["id"]
    print(current_user["token_data"])
    user_email=db.query(models.User).filter(models.User.id==id).first()
    cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email).all()

    return cart_all

@router.put("/increase_cart_item")
def increase_item_cart(cart_increase:schemas.CartIncresase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==cart_increase.product_name)
        if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
        cart_value=cart_all.first().product_quantity

        cart_all.update({"product_quantity":cart_value+1},synchronize_session=False)
        db.commit()
        return {"status":"ok"}

@router.put("/decrease_cart_item")
def increase_item_cart(cart_increase:schemas.CartIncresase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==cart_increase.product_name)
        if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
        cart_value=cart_all.first().product_quantity
        cart_all.update({"product_quantity":cart_value-1},synchronize_session=False)
        db.commit()
        return {"status":"ok"}
@router.get("/delete_cart_item/{name}")
def delete_item_cart(name:str,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==name)
        if cart_all.first()==None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"cart item with name:{name} not found")
        cart_all.delete(synchronize_session=False)
        db.commit()
        return {"message":"deleted"}
@router.put("/set_item_size")
def delete_item_cart(size:schemas.ProductSize,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):  
       id=dict(current_user["token_data"])["id"] 
       user_email=db.query(models.User).filter(models.User.id==id).first()
       cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==size.product_name)
       if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
       cart_all.update({"size":size.size},synchronize_session=False)
       db.commit()
       return {"message":"size set"}
     





               
     
            

                 
                 

    
