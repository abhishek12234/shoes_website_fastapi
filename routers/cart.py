from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,Header
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2
from sqlalchemy.exc import IntegrityError
from connection import websocket_connections,websocket_connections_admin

from typing import List, Optional,Union

router=APIRouter()
async def admin_signal():
       for client in websocket_connections_admin:
                            try:
                                
                                    await client.send_text("user login")
                                    
                            except Exception as e:
                    # Handle disconnected clients if needed
                                            print("Error",e)
                                            pass
       return

async def client_signal():
       for client in websocket_connections:
                            try:
                                
                                    await client.send_text("user login")
                                    
                            except Exception as e:
                    # Handle disconnected clients if needed
                                            print("Error",e)
                                            pass
       return

@router.post("/add_item_cart",response_model=Union[schemas.CartOut, schemas.OutOfStockMessage])
async def add_item_cart(shoes_id:schemas.CartAdd,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):
    id=dict(current_user["token_data"])["id"]
    print(current_user["token_data"])
    user_email=db.query(models.User).filter(models.User.id==id).first()
    shoes=db.query(models.Shoes).filter(models.Shoes.id==shoes_id.id).first()
    print(user_email.email)
    cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email).all()
    new_item=models.Cart(product_id=shoes.id,owner_email=user_email.email,owner_id=id,product_image=shoes.product_image,price=shoes.price,product_name=shoes.name, shoes_category=shoes.shoes_category)
    shoes_stock=db.query(models.Shoes).filter(models.Shoes.id==shoes_id.id).first().shoes_stock
    try:
        if shoes_stock!=0:
                db.add(new_item)
                db.commit()
                db.refresh(new_item)
                if str(origin)=="http://localhost:3001":
                # Iterate over connected WebSocket clients and send a message
                   await client_signal()
                return new_item
        else:
               return {"status":"out of stock"}
    except IntegrityError as e:
        db.rollback()
        
        raise HTTPException(status_code=400, detail="Unique constraint violation: Item already exists")
    
   
@router.get("/all_cart_items",response_model=List[schemas.CartOut])
def add_item_cart(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):
    id=dict(current_user["token_data"])["id"]
    print(current_user["token_data"])
    user_email=db.query(models.User).filter(models.User.id==id).first()
    cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email).all()

    return cart_all

@router.put("/increase_cart_item")
async def increase_item_cart(cart_increase:schemas.CartIncresase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==cart_increase.product_name)
        shoes_stock=db.query(models.Shoes).filter(models.Shoes.name==cart_increase.product_name).first().shoes_stock
      
        if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
        cart_value=cart_all.first().product_quantity
        if shoes_stock<=cart_value:
             return {"status":"not in stock"}
             

        cart_all.update({"product_quantity":cart_value+1},synchronize_session=False)
        db.commit()
        if str(origin)=="http://localhost:3001":
         # Iterate over connected WebSocket clients and send a message
         await client_signal()
        return {"status":"ok"}

@router.put("/decrease_cart_item")
async def increase_item_cart(cart_increase:schemas.CartIncresase,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==cart_increase.product_name)
        if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
        cart_value=cart_all.first().product_quantity
        cart_all.update({"product_quantity":cart_value-1},synchronize_session=False)
        db.commit()
        if str(origin)=="http://localhost:3001":
         # Iterate over connected WebSocket clients and send a message
         await client_signal()
        return {"status":"ok"}
@router.get("/delete_cart_item/{name}")
async def delete_item_cart(name:str,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):
        id=dict(current_user["token_data"])["id"] 
        user_email=db.query(models.User).filter(models.User.id==id).first()
        cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==name)
        if cart_all.first()==None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"cart item with name:{name} not found")
        cart_all.delete(synchronize_session=False)
        db.commit()
        if str(origin)=="http://localhost:3001":
         # Iterate over connected WebSocket clients and send a message
         await client_signal()
        return {"message":"deleted"}
@router.put("/set_item_size")
async def delete_item_cart(size:schemas.ProductSize,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),origin: str = Header(None)):  
       id=dict(current_user["token_data"])["id"] 
       user_email=db.query(models.User).filter(models.User.id==id).first()
       cart_all=db.query(models.Cart).filter(models.Cart.owner_email==user_email.email, models.Cart.product_name==size.product_name)
       if cart_all.first()==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
       cart_all.update({"size":size.size},synchronize_session=False)
       db.commit()
       if str(origin)=="http://localhost:3001":
         # Iterate over connected WebSocket clients and send a message
         await client_signal()
       return {"message":"size set"}
     





               
     
            

                 
                 

    
