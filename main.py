import requests
from fastapi import FastAPI
const port = process.env.PORT || 4000 


app = FastAPI()

def read_root():
    return {"message": "Welcome to my API"}
