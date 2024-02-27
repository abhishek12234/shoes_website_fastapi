from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,WebSocket,Header,BackgroundTasks,WebSocketDisconnect,Request
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2

from typing import List, Optional



router=APIRouter()

@router.get("/all_order")
def add_shoes_to_cart(db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    orders=db.query(models.Orders).all()
    return orders
@router.post("/add_order")
def add_order(order:schemas.OrderAdd,db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    id=dict(current_user["token_data"])["id"]
    user_email=db.query(models.User).filter(models.User.id==id).first()
    new_order=models.Orders(owner_email=user_email.email,**order.dict())
    print(vars(new_order))
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return {"status":"ok"}
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
def update_status(id:int,order_status:schemas.status_update,db: Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user)):
    order_query=db.query(models.Orders).filter(models.Orders.order_id==id)
    order=order_query.first()
    if order==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    order_query.update(order_status.dict(),synchronize_session=False)
    db.commit()
    return {"data":"sucess"}
