import requests
from fastapi import FastAPI

app = FastAPI()

def read_root():
    return {"message": "Welcome to my API"}
