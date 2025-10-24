from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.routes import router as todo_router

app = FastAPI(title="FastAPI MongoDB Todo App")

# Allow React frontend
origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI  Todo App!"}
