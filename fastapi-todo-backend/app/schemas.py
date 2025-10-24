# - **BaseModel** → base class for defining schemas  
# - **Field** → lets you add extra info or validation (like `min_length`, `max_length`)  
# - **Optional** → means that field is not mandatory  
# - **ObjectId** → MongoDB’s unique ID format  

from pydantic import BaseModel, Field # type: ignore
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    

#without Pydantic 
#def create_todo(data):
    # title = data["title"]
    # description = data["description"]
    # If user sends number instead of string → Error
# with Pydantic
# class Todo(BaseModel):
#     title: str
#     description: str

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False


#### Explanation:
# - `title: str` → must be a string  
# - `Field(..., min_length=1, max_length=100)` → required (`...`) and must be between 1–100 chars  
# - `description: Optional[str] = None` → can be empty  
# - `completed: bool = False` → default value is `False`

class TodoCreate(TodoBase):
    pass

# This means TodoCreate has the same fields as TodoBase.
# It’s used for incoming requests when creating a new todo.

class TodoResponse(TodoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True


#### Explanation:

# This is the **response model** — what you send back to the frontend.

# - `id` → uses MongoDB’s `_id` but renames it to `id` in JSON.
# - `json_encoders` → tells FastAPI how to **convert ObjectId → string**
# - `allow_population_by_field_name` → allows `_id` to map correctly to `id`

# So when MongoDB sends this:
# ```python
# {"_id": ObjectId("abc123"), "title": "Test", "completed": False}

# FastAPI will automatically convert it to:

# {"id": "abc123", "title": "Test", "completed": false}