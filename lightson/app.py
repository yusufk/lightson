from fastapi import FastAPI
import os

stage = os.environ.get('STAGE', 'dev')


app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/lightson/{block_id}")
def read_item(block_id: int):
    return {"block_id": block_id}