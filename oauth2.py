import jwt
from datetime import datetime,timedelta
import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from typing import Dict,Any

from sqlalchemy import select
from config import settings
oauth2_scheme= OAuth2PasswordBearer(tokenUrl='login_admin')

target_endpoint = '/login_admin'

# Function to check if an endpoint is present in the app



  
SECREAT_KEY = settings.secret_key
ALGORITHM = settings.algorithm
print(oauth2_scheme)
ACCESS_TOKEN_EXPIRE_MINUTES=1
def create_access_token(data: Dict[str, Any]):
    to_encode=data.copy()
    print(data)
    expire=datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(data, SECREAT_KEY, 'HS256')
    return encoded_jwt
def verify_access_token(token: str,credintials_exception):
        try:
           payload = jwt.decode(token, SECREAT_KEY, algorithms=[ALGORITHM])
        except Exception as e:
             print(e) 
             raise HTTPException(status_code=403, detail=f"error: {e}")
       
        role:str=payload.get("role")
        id:str=payload.get("user_id")
        print(id,role)
        if id is None or role is None:
            raise credintials_exception
        token_data=schemas.Token_data(id=id,role=role)
      
        
        return token_data
async def get_current_user(token:dict=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credintials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credential"
    ,headers={"WWW-Authenticate":"Bearer"})
   
    print(token)
    token= verify_access_token(token,credintials_exception)
   
    user=db.query(models.User).filter(models.User.id == token.id).first()
   
    return {"user":user,"token_data":token}

