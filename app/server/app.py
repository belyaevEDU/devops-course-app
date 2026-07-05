from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from prometheus_client import start_http_server
from prometheus_fastapi_instrumentator import Instrumentator

from os import getenv

import requester
from . import query_validation
from . import logging_setup

HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
INVALID_CURRENCY_MESSAGE = "Invalid currency query"
INVALID_DATE_MESSAGE = "Invalid date query"

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_http_server(9100)
    yield

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app)

logger = logging_setup.make_logger(__name__)

@app.get("/info")
def serve_info():
    info = {
        "version": getenv("VERSION", default="1.0.0"),
        "service": "currency",
        "author": getenv("AUTHOR", default="v.belyaev")
    }
    return form_response(content=info, status_code=HTTP_STATUS_OK) # just for consistency

@app.get("/info/currency")
def serve_currency_data(currency: str = "", date: str = ""):
    result = {
        "service": "currency",
        "data": {}
    }

    responseStatusCode = HTTP_STATUS_OK
    errorMessage = ""

    status = True # going through checkpoints. geniunely couldn't figure out a better way while keeping all features intact

    if currency != "" and not query_validation.validate_currency_name(currency):
        status = False
        errorMessage = INVALID_CURRENCY_MESSAGE
    if date != "" and not query_validation.validate_date(date):
        status = False
        if errorMessage != "":
            errorMessage += " & " + INVALID_DATE_MESSAGE.lower() # adding to the existing error message if there's already one
        else:
            errorMessage = INVALID_DATE_MESSAGE

    if not status: # checkpoint 1: query valid
        responseStatusCode = HTTP_STATUS_BAD_REQUEST
        result["error"] = errorMessage
        return form_response(result, responseStatusCode)

    data = {}
    try:
        data = requester.get_bank_api_response(currency, date)
        result["data"] = data
    except Exception as e:
        status = False
        errorMessage = str(e)
        logger.error(str(e) + "; " + currency + "; " + date) # the only exception expected to reach here is "empty data"/"currency not found"

    if not status: # checkpoint 2: response valid
        responseStatusCode = HTTP_STATUS_BAD_REQUEST
        result["error"] = errorMessage

    return form_response(result, responseStatusCode)

def form_response(content, status_code):
    """
    Helper function for creating a JSONResponse object, containing all needed arguments.
    Exists to give an exact set of needed arguments to create a response to serve.
    """
    return JSONResponse(content=content, status_code=status_code)
