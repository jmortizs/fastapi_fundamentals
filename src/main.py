from enum import Enum
from typing import Optional

from fastapi import Body, Cookie, Form, File, Header, Path, Query, UploadFile
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import status
from pydantic import BaseModel, EmailStr, Field

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

class LoginOutput(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, example='jmos')
    message: str = Field(default='Logging Succesfuly!')

@app.get(path='/', status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

# Request and response body
@app.post(path='/person/new', response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)): # ... means that is required
    return person

# Validations: Query parameters
@app.get(path='/person/detail', status_code=status.HTTP_200_OK)
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
person_ids = [1, 2, 3, 4, 5]

@app.get(path='/person/detail/{person_id}', status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the person identification number. Greater than 1. Required'
        )
):
    if person_id not in person_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This doesn't exists")

    return {person_id: 'It exists'}

# Validations: request body
@app.put(path='/person/{person_id}', status_code=status.HTTP_200_OK)
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

# Forms
@app.post(path='/loging', response_model=LoginOutput, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):

    return LoginOutput(username=username)

# Cookies and headers
@app.post(path='/contact', status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(..., max_length=20, min_length=1),
    last_name: str = Form(..., max_length=20, min_length=1),
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
    ):

    return user_agent

# Files
@app.post(path='/post-image')
def post_image(image: UploadFile = File(...)):

    return {
        'filename': image.filename,
        'format': image.content_type,
        'size(kb)': round(len(image.file.read())/1024, ndigits=2)
    }