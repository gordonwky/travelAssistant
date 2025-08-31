from pydantic_settings import BaseSettings
from pydantic import PostgresDsn,computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

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

    class Config:
        env_file = ".env"

settings = Settings()
