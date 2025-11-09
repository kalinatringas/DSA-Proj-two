from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import traceback
from cosineSim import CosineSimAlgo as algo
from heaps import Heap
import logging
import io
import contextlib

app = FastAPI()

logging.basicConfig(level=logging.INFO) # enables logging for debugging

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
async def root():
    return {"ok": True, "message": "Backend is running"}
import os
import tempfile

@app.post("/reccomend")