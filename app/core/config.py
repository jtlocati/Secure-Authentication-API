from pydantic_settings import BaseSettings, SettingsConfigDict


#Fixes an error when initalizing the settings class into the docker container.

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MIN: int = 60

# call the settings class to directly load JWT environment variables
settings = Settings()
