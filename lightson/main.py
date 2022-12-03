import uvicorn
from fastapi import FastAPI
import os
import logging
from dapr.clients import DaprClient
import json

logging.basicConfig(level=logging.INFO)
env = os.environ.get('ENVIRONMENT', 'dev')

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/lightson/{block_id}")
def read_item(block_id: int):
    logging.info('ligthson service called')
    with DaprClient() as d:
        d.wait(5)
        try:
            if block_id:
                # Get the blocks status from Cosmos DB via Dapr
                state = d.get_state(store_name='blocks', key=block_id)
                if state.data:
                    resp = json.loads(state.data)
                else:
                    resp = json.loads('no block with that id found')
                resp.status_code = 200
                return resp
            else:
                resp = json.loads('Block "id" not found in query string')
                resp.status_code = 500
                return resp
        except Exception as e:
            logging.info.info(e)
            return str(e)
        finally:
            logging.info('completed block call')
    return {"block_id": block_id}

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("lightson.main:app", host="0.0.0.0", port=80, reload=True)
