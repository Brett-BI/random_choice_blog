from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = 'Random Choice'
    db_name: str = ''
    db_username: str = ''
    db_password: str = ''

    class Config():
        env_file = '.env'