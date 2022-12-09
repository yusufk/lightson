import uvicorn
from fastapi import FastAPI, Response, status
from dapr.ext.fastapi import DaprApp
import os
import logging
from dapr.clients import DaprClient
import json

logging.basicConfig(level=logging.INFO)
env = os.environ.get('ENVIRONMENT', 'dev')
DAPR_STORE_NAME = "statestore"

app = FastAPI()
dapr_app = DaprApp(app)

@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/lightson/{block_id}", status_code=status.HTTP_200_OK)
def read_item(block_id: str, response: Response):
    logging.info('ligthson service called')
    with DaprClient() as client:
        client.wait(5)
        try:
            if block_id:
                # Get the blocks status from Cosmos DB via Dapr
                state = client.get_state(DAPR_STORE_NAME, key=block_id)
                if state.data:
                    return {block_id:state.data}
                else:
                    response.status_code = status.HTTP_404_NOT_FOUND
                    return {"error": "Block not found"}
            else:
                response.status_code = status.HTTP_406_NOT_ACCEPTABLE
                return {"error": "Missing block_id"}
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            logging.info(e)
            return str(e)
        finally:
            logging.info('completed block call')
    return {"block_id": block_id}

# API method to save a state of a block
@app.post("/lightson/{block_id}/{status}", status_code=status.HTTP_200_OK)
def save_item(block_id: str, status: str, response: Response):
    logging.info('ligthson service called')
    with DaprClient() as client:
        client.wait(5)
        try:
            if block_id:
                # Save the blocks status from Cosmos DB via Dapr
                state = client.save_state(DAPR_STORE_NAME, key=block_id, value=status)
                return {block_id:status}
            else:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"error": "Missing block_id"}
        except Exception as e:
            logging.info(e)
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return str(e)
        finally:
            logging.info('completed block call')
    return {"block_id": block_id}

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("lightson.main:app", host="0.0.0.0", port=80, reload=True)
