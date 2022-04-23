from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query
from fastapi import Body

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
def home():
    return {"Hello": "World"}

# Request and response body
@app.post('/person/new')
def creaate_person(person: Person = Body(...)): # ... means that is required
    return person

# Validations: Query parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(default=None, min_length=1, max_length=50),
    age: int = Query(...) # query parameters are usually optional, if it is required then it must be a path parameters
):
    return {name: age}