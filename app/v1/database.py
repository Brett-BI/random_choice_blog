from peewee import *
from playhouse.shortcuts import model_to_dict

from datetime import datetime
from typing import Dict, List

from config import Settings

settings = Settings()
#db = PostgresqlDatabase('RCv2', user='postgres', password='password')
db = PostgresqlDatabase(settings.db_name, user=settings.db_username, password=settings.db_password)

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    full_name = CharField()
    email = CharField()
    about = TextField()
    password = CharField()
    created_date = DateTimeField(default=datetime.now)
    active = BooleanField(default=True)

    def create(self) -> None:
        self.save()
        return self


    @staticmethod
    def hash_password(text_password):
        from passlib.context import CryptContext

        password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

        return password_context.hash(text_password)


class Author(BaseModel):
    name = CharField()
    email = CharField()
    about = TextField()


class Article(BaseModel):
    title = CharField(max_length=250)
    subtitle = CharField(max_length=250)
    posted_date = DateTimeField(default=datetime.now)
    summary = CharField(max_length=250)
    markup_content = TextField()
    author = ForeignKeyField(User, lazy_load=False) # lazy load assumes we're using the ID field in Author


    def create(self) -> None:
        self.save()

    
    def update_article(self, article) -> None:
        _article = Article(**article.dict())
        _article.save()
    

    def get_article(self, article_id: int) -> Dict:
        _article = self.select(Article, User.id, User.full_name).join(User).where(Article.id == article_id).limit(1)
        if _article:
            return _article[0]
        else:
            return None
        #return self.select().filter_by(self.id == article_id).join(User, on=(self.author == User.id)).limit(1)

    
    def get_articles(self, count: int = 1) -> List[dict]:
        _articles = self.select(Article, User.id, User.full_name).join(User).order_by(Article.posted_date.desc()).limit(count) # self.posted_date doesn't work for some reason...
        models = []
        for _a in _articles:
            _author = _a.author.__data__
            #print(f'_author is: {_author}')
            _temp_article = _a.__data__
            #print(f'_temp_article is: {_temp_article}')
            _temp_article['author'] = _author
            #print(_temp_article)
            models.append(_temp_article)
        
        return models


    def get_random_article(self, count: int = 1) -> List[dict]:
        _articles = self.select().order_by(fn.Random()).limit(count)
        print(_articles.__dict__)
        models = []
        for _a in _articles:
            print(type(_a))
            print(_a.__dict__)
            models.append(_a.__data__)
            #_m = model_to_dict(_articles)
            #models.append(_m)
        
        print(models)
        return models
        # for _a in _articles._from_list:
        #     print(_a)
        #     print(_a)


#db.create_tables([Person])