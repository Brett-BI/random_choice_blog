from pydantic import BaseModel

class ArticleRequestModel(BaseModel):
    title: str
    subtitle: str
    author: int = 1
    markup_content: str


class ArticleResponseModel(BaseModel):
    title: str
    subtitle: str
    markup_content: str
    posted_date: str
    author: int


class Article(BaseModel):
    title: str
    subtitle: str
    markup_content: str
    posted_date: str
