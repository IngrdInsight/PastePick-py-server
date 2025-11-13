import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # S3/Allas
    ALLAS_ENDPOINT = os.getenv("ALLAS_ENDPOINT")
    ALLAS_ACCESS_KEY = os.getenv("ALLAS_ACCESS_KEY")
    ALLAS_SECRET_KEY = os.getenv("ALLAS_SECRET_KEY")
    ALLAS_BUCKET = os.getenv("ALLAS_BUCKET")

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Image processing
    TARGET_SIZE = (800, 800)
    IMAGE_FORMAT = "webp"
    IMAGE_QUALITY = 85


config = Config()