from pydantic  import BaseModel
from typing import Optional 

class UserCreateSchema(BaseModel):
    first_name: str
    username: str
    last_name: str
    altura: int
    edad: int
    sexo: str
    actividad: str
    objetivo: str 
    weekly_plan: str 