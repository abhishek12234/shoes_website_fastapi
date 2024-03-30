from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,Header
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,oauth2
from sqlalchemy.exc import IntegrityError
from utils import pwd_context
from typing import List


from connection import websocket_connections,websocket_connections_admin
import websockets


from sqlalchemy import select



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



@router.get("/allusers",response_model=List[schemas.UserInfo])
async def get_all_users(db:Session = Depends(get_db),current_user:dict=Depends(oauth2.get_current_user),origin: str = Header(None)):
    print(str(origin),"---------------")
    if dict(current_user["token_data"])["role"]!="admin":
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"only admin have access")
    print(str(origin)!="http://localhost:3000")
    if str(origin)=="http://localhost:3001":
      for client in websocket_connections_admin:
          try:
              await client.send_text("item added")
          except websockets.exceptions.ConnectionClosedError:
              pass  # Handle disconnected clients if needed
          
   
    all_users=db.query(models.User).all()
    
    return all_users
  

@router.post("/users",response_model=schemas.UserOut)
async def create_post(users:schemas.UserCreate,db: Session= Depends(get_db),origin: str = Header(None)):
    hashed_password=pwd_context.hash(users.password)
    users.password=hashed_password
    try:
        new_user=models.User(**users.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(new_user,"+++++++++++++++++++++++++++++++++")

        if str(origin)!="http://localhost:3000":
            await admin_signal()
        return new_user
    
   
    except IntegrityError as e:
        # Handle the unique constraint violation error
          # Rollback the transaction to avoid database changes
        db.rollback()  # Rollback the transaction to avoid database changes
        raise HTTPException(status_code=400, detail="Unique constraint violation: User with the same unique field already exists.")
    

@router.get("/delete_user/{id}")
def read(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    
    user_query=db.query(models.User).filter(models.User.id==id)
    user=user_query.first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted"} 
@router.post("/add_address")
def address(address:schemas.AddAddress,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    id=dict(current_user["token_data"])["id"] 
    user_query=db.query(models.User).filter(models.User.id==id)
    user=user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    user_query.update({"user_address":address.user_address},synchronize_session=False)
        
    db.commit()
    return {"message":"address updates"} 
@router.post("/add_number")
def address(number:schemas.AddNumber,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    id=dict(current_user["token_data"])["id"] 
    user_query=db.query(models.User).filter(models.User.id==id)
    user=user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    user_query.update({"user_phone_no":number.user_phone_no},synchronize_session=False)
        
    db.commit()
    return {"message":"number updates"} 

@router.post("/add_name")
def address(name:schemas.AddName,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    id=dict(current_user["token_data"])["id"] 
    user_query=db.query(models.User).filter(models.User.id==id)
    user=user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    user_query.update({"user_name":name.user_name},synchronize_session=False)
        
    db.commit()
    return {"message":"name updates"} 

@router.get("/current_user_info",response_model=schemas.CurrentUserInfo)
def address(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    id=dict(current_user["token_data"])["id"] 
    user_query=db.query(models.User).filter(models.User.id==id)
    user=user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    
    
        
    
    return user