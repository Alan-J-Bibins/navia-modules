from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_gemini_api_key: str = ""
    hf_token:str = ""
    opencode_api_key:str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    fanar_api_key:str = ""

settings = Settings()
