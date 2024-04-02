from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,Header
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2
from connection import websocket_connections,websocket_connections_admin

from typing import List, Optional



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
@router.get("/all_order")
def add_shoes_to_cart(db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    orders=db.query(models.Orders).all()
    return orders
@router.get("/current_user_all_order")
def add_shoes_to_cart(db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    id=dict(current_user["token_data"])["id"]
    orders=db.query(models.Orders).filter(models.Orders.owner_id==id).all()
    return orders
@router.post("/add_order")
async def add_order(order:schemas.OrderAdd,db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user),origin: str = Header(None)):
    id=dict(current_user["token_data"])["id"]
    user_email=db.query(models.User).filter(models.User.id==id).first()
    cart_items=db.query(models.Cart).filter(models.Cart.owner_id==id).all()
    products=db.query(models.Shoes).all()
    for cart_item in cart_items:
        # Create an order item with data from the cart item
        order_item = models.Orders()
        for column in models.Orders.__table__.columns:
            if hasattr(cart_item, column.name):
                setattr(order_item, column.name, getattr(cart_item, column.name))
        
        # Manually set additional attributes for the order item
         # Set the order ID for the order item
        shoes_stock=db.query(models.Shoes).filter(models.Shoes.id==cart_item.product_id).first().shoes_stock
        if shoes_stock>=cart_item.product_quantity:
            db.query(models.Shoes).filter(models.Shoes.id==cart_item.product_id).update({"shoes_stock":shoes_stock-cart_item.product_quantity},synchronize_session=False)
        
        order_item.user_address = order.user_address
        order_item.payment = order.payment 
        order_item.shipping_method = order.shipping_method
        order_item.owner_id=id
        order_item.owner_name=user_email.user_name
        order_item.owner_email = user_email.email   # Set additional attribute
        
        db.add(order_item)
    db.query(models.Cart).filter(models.Cart.owner_id==id).delete(synchronize_session=False)
    
   
   
    db.commit()
    if str(origin)=="http://localhost:3001":
        # Iterate over connected WebSocket clients and send a message
        await admin_signal()
    
    
    return order_item
@router.get("/delete_order/{id}")
def delete_order(id:int,db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
     order_query=db.query(models.Orders).filter(models.Orders.order_id==id)
     order=order_query.first()
     if order==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
     order_query.delete(synchronize_session=False)
     db.commit()
     return {"message":"deleted"}
@router.put("/update_status/{id}")
async def update_status(id:int,order_status:schemas.status_update,db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user),origin: str = Header(None)):
    order_query=db.query(models.Orders).filter(models.Orders.order_id==id)
    order=order_query.first()
    if order==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    order_query.update(order_status.dict(),synchronize_session=False)
    db.commit()
    if str(origin)=="http://localhost:3000":
        # Iterate over connected WebSocket clients and send a message
        await client_signal()
    return {"data":"sucess"}

