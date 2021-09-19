from pydantic import BaseModel

from typing import Optional, Dict

class ArticleRequestModel(BaseModel):
    id: Optional[str]
    title: str
    subtitle: str
    author: int = 1
    markup_content: str


class ArticleResponseModel(BaseModel):
    id: str
    title: str
    subtitle: str
    markup_content: str
    posted_date: str
    author: Dict


class Article(BaseModel):
    title: str
    subtitle: str
    markup_content: str
    posted_date: str
