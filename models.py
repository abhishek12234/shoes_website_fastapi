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
    shoes_stock=Column(Integer,server_default=text('0'))
    shoes_description=Column(String,server_default=text("''"))
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    login_status = Column(Boolean, nullable=False, server_default=text('false'))  # Changed to lowercase 'false'
    online_status = Column(Boolean, nullable=False, server_default=text('false'))  # Changed to lowercase 'false'
    total_quantity = Column(Integer, nullable=False, server_default=text('0'))
    total_purchase = Column(Integer, nullable=False, server_default=text('0'))
    user_address = Column(String, nullable=False, server_default=text("'None'"))  # Added single quotes around 'None'
    user_phone_no = Column(String, nullable=False, server_default=text("''"))  # Set default to empty string

class Admin(Base):
    __tablename__="admin"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, nullable=False)
    owner_name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner_email = Column(String, nullable=False)
    user_address = Column(String, nullable=False, server_default=text("'None'"))
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    product_image = Column(Text, nullable=False)
    shoes_category = Column(String, nullable=False)
    size = Column(Integer, nullable=False, server_default=text("9"))
    product_quantity = Column(Integer, nullable=False, server_default=text("1"))
    order_status = Column(String, nullable=False, server_default=text("'processing'"))
    payment = Column(String, nullable=False)
    shipping_method = Column(String, nullable=False, server_default=text("'processing'"))
    ordered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    
class Cart(Base):
    __tablename__ = "cart"
    order_id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("shoes.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner_email = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False, server_default=text("9"))
    product_image = Column(Text, nullable=False)
    shoes_category = Column(String, nullable=False)
    product_quantity = Column(Integer, nullable=False, server_default=text("1"))

    
 

    
    
   
