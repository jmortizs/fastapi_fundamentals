from typing import Optional
from enum import Enum
from unicodedata import name
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from fastapi import FastAPI
from fastapi import Query
from fastapi import Body
from fastapi import Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    red = 'red'
    blonde = 'blonde'

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, title='Person Name')
    last_name: str = Field(..., min_length=1, max_length=50, title='Person Name')
    age: int = Field(..., gt=0, le=120)
    email: EmailStr = Field(...)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonBase):
    password: str = Field(..., min_length=8)

class PersonOut(PersonBase):
    pass

class Location(BaseModel):
    city: str
    state: str
    country: str

@app.get('/')
def home():
    return {"Hello": "World"}

# Request and response body
@app.post('/person/new', response_model=PersonOut)
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

# Validations: request body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        get=0,
        title='Person ID',
        description='This is the person identification number. Greater than 1. Required'
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results