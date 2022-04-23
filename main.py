from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query
from fastapi import Body
from fastapi import Path

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
def create_person(person: Person = Body(...)): # ... means that is required
    return person

# Validations: Query parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title='Person Name.',
        description='This is the person name. length must be between 1 and 50 characters.'
        ),
    age: int = Query(
        ...,
        title='Person age.',
        description='This is the person age. Grater than 0. Requiered.'
        ) # query parameters are usually optional, if it is required then it must be a path parameters
    ):
    return {name: age}

# Validations: path parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the person identification number. Greater than 1. Required'
        )
    ):
    return {person_id: 'It exists'}