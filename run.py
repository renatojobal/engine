import logging
from app.config import config_dict
from app import create_app
from decouple import config
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# WARNING: Don't run with debug turned on in production.
DEBUG = config('DEBUG', default=True, cast=bool)

# Set configuration values
config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[config_mode.capitalize()]

    logging.basicConfig(level=logging.DEBUG)
except KeyError:
    exit('Error: Invalid <config mode>. Expected values -> [Debug, Production]')

app = create_app(app_config)
Migrate(app)

if __name__ == '__main__':
    app.run()
