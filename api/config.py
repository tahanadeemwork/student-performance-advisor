# ============================================
# Flask Configuration
# ============================================

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY         = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG              = os.getenv("DEBUG", "True") == "True"
    CORS_ORIGINS       = os.getenv("CORS_ORIGINS", "http://localhost:5173")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production" : ProductionConfig,
    "default"    : DevelopmentConfig
}