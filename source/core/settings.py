from decouple import config


class Settings:
    POSTGRES_USER = config('POSTGRES_USER')
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    POSTGRES_HOST = config('POSTGRES_HOST')
    POSTGRES_DB_NAME = config('POSTGRES_DB_NAME')
    POSTGRES_PORT = config('POSTGRES_PORT')

    DATABASE_URL = \
        f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}'

    SELENIUM_HOST = config('SELENIUM_HOST')
    WILDAUTHNEW_V3 = config('WILDAUTHNEW_V3')
    REDIS_URL = config('REDIS_URL')


settings = Settings()
