from fastapi import APIRouter, HTTPException # type: ignore
from app.database import todos_collection
from app.schemas import TodoCreate, TodoResponse
from bson import ObjectId # type: ignore

router = APIRouter(prefix="/api/todos", tags=["Todos"])

@router.get("/", response_model=list[TodoResponse])
def get_todos():
    todos = list(todos_collection.find())
    return todos

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    new_todo = todo.dict()
    result = todos_collection.insert_one(new_todo)
    created_todo = todos_collection.find_one({"_id": result.inserted_id})
    return created_todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoCreate):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = todos_collection.update_one(
        {"_id": ObjectId(todo_id)}, {"$set": todo.dict()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated = todos_collection.find_one({"_id": ObjectId(todo_id)})
    return updated

@router.delete("/{todo_id}")
def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = todos_collection.delete_one({"_id": ObjectId(todo_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}
