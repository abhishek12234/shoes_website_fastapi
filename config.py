from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_password: str = "0786"
    database_name: str = "shoes_database"
    database_username: str = "postgres"
    secret_key: str = "0dca03efgds"
    algorithm: str = "HS256"
    database_port: str = "5432"
    aws_secret_key: str = "EXLJLOOGZYHM5EeUNXjSWzzYJg0H7z6hpngX0uaa"

settings = Settings()