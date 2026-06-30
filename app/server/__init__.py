import uvicorn
from os import getenv

def run():
    uvicorn.run("server.app:app", host="0.0.0.0", port=int(getenv("PORT", default="8000")))