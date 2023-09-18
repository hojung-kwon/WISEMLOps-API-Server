import ssl

from src.config import Config

ssl._create_default_https_context = ssl._create_unverified_context
app_config = Config()
