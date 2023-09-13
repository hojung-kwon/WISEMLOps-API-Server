from src import app_config

MODULE_CODE = 107


def get_sqlalchemy_database_url():
    return app_config.SQLALCHEMY_DATABASE_URL
