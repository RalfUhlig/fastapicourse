# Do not check this into a source code repository like git.

from pydantic import BaseSettings

# Class to hold all environment variables.
# https://youtu.be/0sOvCWFmrtA?t=32740
class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str

    secret_key: str
    signing_algorithm: str
    access_token_expire_minutes: int

    # Read the configuration from an environment file.
    # Requires python-dotenv to be installed.
    class Config:
        env_file = ".env"


# Getting an instance of the Settings class.
settings = Settings()

# Source for environment variables:
#   Default values of the class variables
#   .env file
#   System environment variables
