import requests
from fastapi import FastAPI



app = FastAPI()

port = process.env.PORT || 4000 
def read_root():
    return {"message": "Welcome to my API"}
