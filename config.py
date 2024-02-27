from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_password: str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    class Config:
        env_file=".env"
    
settings=Settings()
print(settings.database_hostname)