from fastapi import FastAPI,Depends,HTTPException
from fastapi.params import Body


from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from sqlalchemy import text
import schemas
from typing import List, Set
from routers import post,user,auth,order,cart
import socketio


models.Base.metadata.create_all(bind=engine)

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(order.router)
app.include_router(cart.router)

print("hello")







    
    



