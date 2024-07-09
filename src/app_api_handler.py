import asyncio
import aiohttp
import uvicorn
import os
import aiofiles
from pydantic import BaseModel
from fastapi import FastAPI
from chatbot_app.query_rag import QueryResponse, query_rag
from chatbot_app.populate_database import populate
from chatbot_app.download_pdf import process_attachments

app = FastAPI()

class SubmitQueryRequest(BaseModel):
    query_text: str

@app.get("/")
def index():
    return {"data": "Hello World"}

@app.post("/submit_query")
def submit_query(request: SubmitQueryRequest) -> QueryResponse:
    response = query_rag(request.query_text)
    return response

@app.get("/update")
def update():
    populate()

@app.get("/download")
async def download(data):
    await process_attachments(data)



if __name__ == "__main__":
    try:
        port = 5050
        print(f"Starting server on port {port}")
        uvicorn.run("app_api_handler:app", host="localhost", port=port)
    except KeyboardInterrupt as e:
        print("Server stopped.")