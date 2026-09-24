from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Base de Datos
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str
    
    # MinIO
    MINIO_USER: str
    MINIO_PASSWORD: str
    MINIO_HOST: str = "localhost:9000"
    MINIO_BUCKET: str = "sgc-documentos"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Construye la URL de conexión para SQLAlchemy
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Lee las variables del archivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()