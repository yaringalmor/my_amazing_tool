import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from typing import Union

WELCOME_MSG = """Welcome to My Amazing Tool!<br>
Please send us your favorite content, and it will be display in short time.<br>
Thanks for chossing My Amazing Tool!"""

app = FastAPI()
client = MongoClient(host=os.environ.get('MONGODB_HOST'),
                     port=int(os.environ.get('MONGODB_PORT')),
                     username=os.environ.get('MONGODB_USERNAME'),
                     password=os.environ.get('MONGODB_PASSWORD'))

db = client[os.environ.get('MONGODB_DATABASE')]
collection = db[os.environ.get('MONGODB_COLLECTION')]


@app.get("/", response_class=HTMLResponse)
def read_root():
    try: 
        content = collection.find_one()['message']
        return content
    except KeyError:
        return WELCOME_MSG