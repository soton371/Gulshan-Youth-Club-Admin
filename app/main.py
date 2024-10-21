from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

