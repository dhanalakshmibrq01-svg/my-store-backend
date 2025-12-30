
from fastapi import FastAPI
 #from enum import Enum #from typing import Optional
from router import employee,department,role,category,product,file
from fastapi.staticfiles import StaticFiles 
from db import models
# from fastapi.responses import JSONResponse
from db.database import engine 
# from fastapi.middleware.cors import CORSMiddleware
app=FastAPI() 



@app.get('/') 
def index():
    return 'product management system'


app.include_router(file.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(role.router) 
app.include_router(category.router)
app.include_router(product.router)

models.Base.metadata.create_all(engine) 

# origins = [
#     "http://localhost:3000",  # frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.mount("/media", StaticFiles(directory="media"), name="media")