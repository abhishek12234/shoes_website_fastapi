from fastapi import FastAPI,Depends,HTTPException,APIRouter,status,WebSocket,Header,BackgroundTasks,WebSocketDisconnect,Request
from sqlalchemy.orm import Session
from sqlalchemy import update,select
import database, schemas, models,utils,oauth2

from connection import websocket_connections,websocket_connections_admin



from jose import JWTError,jwt
router=APIRouter(tags=['Authentication'])



# Start the check_heartbeat background task



SECREAT_KEY = "0dca03efgds"
ALGORITHM = "HS256"

async def user_active(token:str,db:Session,active:bool):
      print(active,"------------------")
      
      
      try:
        payload=jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])
        id,role=payload.get("user_id"),payload.get("role")
        if id is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credential")
        user_query = db.query(models.User).filter(models.User.id == id)
        user = user_query.first()
        print("Before update")
        user_query.update({"online_status": active}, synchronize_session=False)
        print("after update")
        db.commit()
        print("commit update")
        
        
             
             
      except Exception as e:
          raise HTTPException(status_code=403, detail=f"error: {e}")
      return
async def admin_signal():
       for client in websocket_connections_admin:
                            try:
                                
                                    await client.send_text("user login")
                                    
                            except Exception as e:
                    # Handle disconnected clients if needed
                                            print("Error",e)
                                            pass
       return
      
@router.websocket("/ws1")
async def websocket_endpoint(websocket: WebSocket,origin:str=Header(None),db: Session = Depends(database.get_db)):
      
      await websocket.accept()
      if str(origin)=="http://localhost:3000":
          
          websocket_connections_admin.add(websocket)
      else:
           websocket_connections.add(websocket)
      data = await websocket.receive_text()
      token = data.strip()
      print("length",len(websocket_connections),len(websocket_connections_admin))
      await user_active(token=token,db=db,active=True)
      if str(origin)!="http://localhost:3000":
            await admin_signal()
      
      try:
        while True:
            print("'''''''''''''''''''")
            try:
                        data = await websocket.receive_text()
                        await websocket.send_text(f"Received: {data}")
                        print(f"Received data: {data}")
                        
            except Exception as e:
                   
                    print(e)
                        
                    print(origin,"closed")
                    
            # Iterate over connected WebSocket clients and send a message
                    await user_active(token=token,db=db,active=False)
                    await admin_signal()
                    break
      except Exception as e:
           print("error",e)
           pass
      finally:
           if origin=="http://localhost:3000":
                            websocket_connections_admin.remove(websocket)
           else:
                            websocket_connections.remove(websocket)
           
        
@router.post("/login_admin")
def login_admin(admin_cred: schemas.AdminLogin,db: Session = Depends(database.get_db)):
    admin_query=db.query(models.Admin).filter(models.Admin.email==admin_cred.email)
    admin=admin_query.first()
    if not admin:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid credentials")
    if not utils.verify(admin_cred.password, admin.password):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"invalid credentials")
    
    access_token=oauth2.create_access_token(data={"user_id":admin.id,"role":"admin"})
    db.commit()
    
    return {"token":access_token,"status":"ok"}


@router.post("/login_user")
async def login_user(
    user_cred: schemas.UserLogin,
    db: Session = Depends(database.get_db),
    origin: str = Header(None),
):
    print(str(origin))
    print(str(origin) != "http://localhost:3000")

    user_query = db.query(models.User).filter(models.User.email == user_cred.email)
    user = user_query.first()

    if not user:
        return  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials"
        )

    if not utils.verify(user_cred.password, user.password):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials"
        )
 
    user_query.update({"login_status": True}, synchronize_session=False)
    db.commit()
    
    if str(origin) != "http://localhost:3000":
        # Iterate over connected WebSocket clients and send a message
        
        await admin_signal()

    # Update login status in the database
   

    # Create an access token for the user
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "role": "user"}
    )
    
   

    return {"token": access_token, "status": "ok"}



@router.get("/logout_user")
async def logout_user(db: Session = Depends(database.get_db),current_user:dict=Depends(oauth2.get_current_user),origin: str = Header(None)):
    user_id=dict(current_user["token_data"])["id"]
    
    user_query=db.query(models.User).filter(models.User.id==user_id)
    user_query.update({"login_status":False}, synchronize_session=False)
    db.commit()
    
    if str(origin)!="http://localhost:3000":

        await admin_signal()
    
    
    
    return {"status":"ok"}

    

