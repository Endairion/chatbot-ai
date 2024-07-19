import gc
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Request
from chatbot_app.RAGQuery import RAGQuery, QueryResponse
from starlette.middleware.cors import CORSMiddleware

DB_PATH = "data/chroma"

app = FastAPI()

class GCMiddleware:
    def __init__(self, app: FastAPI, threshold: int = 1):
        self.app = app
        self.threshold = threshold
        self.request_count = 0

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            self.request_count += 1
            if self.request_count >= self.threshold:
                gc.collect()
                self.request_count = 0
                print("Garbage collection triggered")

        await self.app(scope, receive, send)

app.add_middleware(GCMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

class SubmitQueryRequest(BaseModel):
    query_text: str

@app.get("/")
def index():
    return {"data": "Hello World"}

@app.post("/submit_query")
def submit_query(request: SubmitQueryRequest) -> QueryResponse:
    with RAGQuery(
        db_path = DB_PATH,
        model_name = "intfloat/multilingual-e5-large",
        model_kwargs = {'device': "cpu"}
    ) as rag:
        return rag.query(request.query_text)
    

# @app.get("/update")
# def update():
#     populate()

# @app.get("/download")
# async def download(data):
#     await process_attachments(data)



if __name__ == "__main__":
    try:
        port = 5050
        print(f"Starting server on port {port}")
        uvicorn.run("app_api_handler:app", host="localhost", port=port)
    except KeyboardInterrupt as e:
        print("Server stopped.")