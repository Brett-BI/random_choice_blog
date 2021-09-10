from peewee import *
from playhouse.shortcuts import model_to_dict

from datetime import datetime
from typing import Dict, List

db = PostgresqlDatabase('RCv2', user='postgres', password='password')


class BaseModel(Model):
    class Meta:
        database = db


class Author(BaseModel):
    name = CharField()
    email = CharField()
    about = TextField()


class Article(BaseModel):
    title = CharField()
    subtitle = CharField()
    posted_date = DateTimeField(default=datetime.now)
    markup_content = TextField()
    author = ForeignKeyField(Author, lazy_load=False) # lazy load assumes we're using the ID field in Author


    def create(self) -> None:
        self.save()
    

    def get_article(self, article_id: int) -> Dict:
        return self.select().filter_by(self.id == article_id).limit(1)

    
    def get_articles(self, count: int = 1) -> List[dict]:
        _articles = self.select().order_by(Article.posted_date.desc()).limit(count) # self.posted_date doesn't work for some reason...
        models = []
        for _a in _articles:
            models.append(_a.__data__)
        
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