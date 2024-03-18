from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,Text,LargeBinary
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import text
from sqlalchemy.orm import relationship

class Shoes(Base):
    __tablename__="shoes"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    price=Column(Integer,nullable=False)
    shoes_type=Column(String,nullable=False)
    product_image=Column(String,nullable=False)
    shoes_category=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
    
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    user_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)

    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    login_status=Column(Boolean,nullable=False,server_default=text('False'))
    online_status=Column(Boolean,nullable=False,server_default=text('False'))
    total_quantity=Column(Integer,nullable=False,server_default=text('0'))
    total_purchase=Column(Integer,nullable=False,server_default=text('0'))
    user_address=Column(String,nullable=False,server_default=text('None'))
class Admin(Base):
    __tablename__="admin"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
class Orders(Base):
    __tablename__="orders"
    order_id=Column(Integer,primary_key=True,nullable=False)
    owner_email=Column(String,ForeignKey("users.email",ondelete="CASCADE"),nullable=False)
    product_name=Column(String,nullable=False)
    price=Column(Integer,nullable=False)
    
    order_status=Column(String,nullable=False,server_default=text("'processing'"))
    payment=Column(String,nullable=False)
    ordered_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
class Cart(Base):
    __tablename__="cart"
    order_id=Column(Integer,primary_key=True,nullable=False)
    owner_email=Column(String,ForeignKey("users.email",ondelete="CASCADE"),nullable=False)
    product_name=Column(String,nullable=False)
    price=Column(Integer,nullable=False)
    size=Column(Integer,nullable=False,server_default=text("9"))
    product_image=Column(Text,nullable=False)
    shoes_category=Column(String,nullable=False)
    product_quantity=Column(Integer,nullable=False,server_default=text("1"))
    

    
    
   
