from time import sleep
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from fastapi.middleware.cors import CORSMiddleware
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from database import Article, Author, User as UserTable, db
from helpers import DefaultConverter
from Models.ArticleModels import ArticleRequestModel, ArticleResponseModel
from Models.UserModels import CreateUserRequestModel, UserResponseModel
from core.auth import Token, authenticate_user, fake_users_db, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, User, oauth2scheme

from datetime import datetime, timedelta
import json
from typing import List, Optional

from config import Settings

settings = Settings()
app = FastAPI(version=1.0, title=settings.app_name)

db = db

db.create_tables([Article])

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    #user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    print(form_data.username)
    print(form_data.password)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer" }


@app.get('/article/random', response_model=List[ArticleResponseModel])
def get_random_article(count: Optional[int] = 1):
    _articles = Article().get_random_article(count)
    return jsonable_encoder(_articles)


@app.get('/article/latest', response_model=List[ArticleResponseModel])
def get_latest_articles(count: Optional[int] = 1):
    _articles = Article().get_articles(count)
    print(_articles)
    for a in _articles:
        print(a)
    #sleep(3)
    return jsonable_encoder(_articles)


# def get_article(article_id, token: str = Depends(oauth2scheme)):
@app.get('/article/{article_id}', response_model=ArticleResponseModel)
def get_article(article_id):
    #_article = Article.get_or_none(Article.id == article_id)
    _article = Article().get_article(article_id)
    _fa = _article.__data__
    _fa['author'] = _article.author.__data__

    return jsonable_encoder(_fa) # note: JSONResponse ignores the response_model


@app.patch('/article/{article_id}', status_code=201, response_model=ArticleResponseModel)
def edit_article(article_id: str, article: ArticleRequestModel):
    print(article)
    print(article_id)
    _article = Article().update_article(article)

    return jsonable_encoder(_article)


@app.post('/article', status_code=201)
def create_article(article: ArticleRequestModel, token=Depends(oauth2scheme)):
    print(article)
    _article = Article(**article.dict())
    _article.create()

    return JSONResponse({'message': 'article received?'})


@app.get('/me')
def get_my_info():
    pass


@app.get('/me/articles')
def get_my_articles():
    pass


@app.post('/users', status_code=201, response_model=UserResponseModel)
def create_user(user: CreateUserRequestModel):
    hashed_pwd = UserTable.hash_password(user.password)
    _temp_user = {
        'full_name': '',
        'email': user.email,
        'about': '',
        'password': hashed_pwd,
        'active': True
    }
    _user = UserTable(**_temp_user)
    _user.create()

    return jsonable_encoder(_user.__data__)


@app.get('/users/me', response_model=UserResponseModel)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    print(current_user.__data__)
    #sleep(2)
    return jsonable_encoder(current_user.__data__)