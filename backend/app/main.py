from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import emissions, upload, chat

app = FastAPI(title="Emissions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5174"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(emissions.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"status":"ok"}
