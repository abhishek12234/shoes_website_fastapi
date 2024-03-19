from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import UploadFile,File,Form
from typing import Optional,List

class PostBase(BaseModel):
    name:str
    price:int
    
class ShoesCreate(BaseModel):
    
    name:str
    price:int
    product_image:str
    shoes_category:str
    shoes_type:str

   
    
    
class CartBase(BaseModel):
    product_image:str
    product_name:str
    price:int
    product_quantity:int
    size:int
class OrderAdd(BaseModel):
    
    
    product_name:str

    
    price:int
   
    payment:str
    
class status_update(BaseModel):
    order_status:str
class UserOut(BaseModel):
    id:int
    email:EmailStr
    class Config:
        from_attributes=True
class CartOut(BaseModel):
    product_name:str
    product_quantity:int
    price:int
    size:int
    product_image:str
    shoes_category:str
    class Config:
        from_attributes=True
class CartIncresase(BaseModel):
    
    product_name:str
    
class AddAddress(BaseModel):
    
    user_address:str 
class ProductSize(BaseModel):
    product_name:str
    size:int 
class CartAdd(BaseModel):
    id: int
class Shoes(BaseModel):
    name:str
    price:int
    product_image: str
    shoes_type:str
    shoes_category:str
    id:int
    
   

    class Config:
        arbitrary_types_allowed = True
class UserCreate(BaseModel):
    user_name:str
    email:EmailStr
    password:str
class UserInfo(BaseModel):
    id:int
    user_name:str
    email:EmailStr
    total_quantity:int
    total_purchase:int
    login_status:bool
    online_status:bool
    created_at:datetime
    class Config:
        from_attributes=True
class CurrentUserInfo(BaseModel):
    
    user_name:str
    email:EmailStr
    user_address:str
    user_phone_no:str 
   
    class Config:
        from_attributes=True 
class Active(BaseModel):
    active_status:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str
class AdminLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class Token_data(BaseModel):
    id:int
    role:str