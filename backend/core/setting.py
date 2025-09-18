from pydantic_settings import BaseSettings
from pydantic import PostgresDsn,computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    REDIS_SERVER: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

    OPENAI_API_KEY: str
    SECRET_KEY: str

    @computed_field
    @property
    def REDIS_DATABASE_URL(self)-> str:
        return str(
            MultiHostUrl.build(
                scheme="redis",
                host=self.REDIS_SERVER,
                port=self.REDIS_PORT,
                path=self.REDIS_DB,
            )
        )
    

    class Config:
        env_file = ".env"

settings = Settings()
