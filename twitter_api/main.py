
from datetime import date, datetime
import json
from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title='twitter api')

# models
class BaseUser(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(BaseUser):
    password: str = Field(..., min_length=8, max_length=64)

class User(BaseUser):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User, UserLogin):
    pass

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., min_length=1, max_length=280)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: BaseUser = Field(...)

# Path operations
## Users
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='register a user',
    tags=['users']
)
def signup_user(user: UserRegister = Body(...)):
    """
    Path operation that register an user in the app.

    Args:
        user (UserRegister, optional): user register **request body**.

    Returns:
        user: user signup information.
    """

    with open('users.json', 'r+', encoding='utf-8') as f:
        results = json.load(f)
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))

    return user


@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='login a user',
    tags=['users']
)
def login_user():
    pass

@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='show all users',
    tags=['users']
)
def show_all_users():
    """
    Path operation that shows all registred users.

    Returns:
        List[User]: list that contains all registred users.
    """
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
        return results

@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='show an user',
    tags=['users']
)
def show_user():
    pass

@app.delete(
    path='/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='deletes an user',
    tags=['users']
)
def delete_user():
    pass

@app.put(
    path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='update an user',
    tags=['users']
)
def update_user():
    pass

## Tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='show all tweets',
    tags=['tweets']
)
def home():
    """
    Path operation that shows all posted tweets.

    Returns:
        List[Tweet]: list all posted tweets.
    """
    with open('tweets.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
        return results

@app.get(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='show a tweet',
    tags=['tweets']
)
def show_tweet():
    pass

@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='post a tweet',
    tags=['tweets']
)
def post_tweet(tweet: Tweet = Body(...)):
    """
    Path operation that post a tweet

    Args:
        tweet (Tweet, optional): tweet **body request**

    Returns:
        tweet: tweet information
    """
    with open('tweets.json', 'r+', encoding='utf-8') as f:
        results = json.load(f)
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict['updated_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))

        return tweet

@app.delete(
    path='/tweet/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='delete a tweet',
    tags=['tweets']
)
def delete_tweet():
    pass

@app.put(
    path='/tweet/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='update a tweet',
    tags=['tweets']
)
def update_tweet():
    pass