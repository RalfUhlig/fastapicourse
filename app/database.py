from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# Database: FastAPICourse
# Server: multibox
# User: FastAPICourse
# Password: FastAPICourse

# Define the MariaDB connection using MariaDB Connector/Python
# Connection string: mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

# Read it from the settings.
# https://youtu.be/0sOvCWFmrtA?t=33475
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://"\
                          f"{settings.database_username}:{settings.database_password}"\
                          f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Define an engine, session class and base class for models.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Helper function to get easy access to the database session.
def get_db():
    db = SessionLocal()

    try:
        # Yield is generally used to convert a regular Python function into a generator.
        yield db
    finally:
        db.close()


# # Classic connection to te database.
# while True:
#     try:
#         # Database credentials will be stored in environment later.
#         conn = mysql.connector.connect(host = "multibox",
#                                        database="FastAPICourse",
#                                        user="FastAPICourse",
#                                        password="FastAPICourse")
#         cursor = conn.cursor(dictionary=True)
#         print("Database connection was successful.")
#         break
#     except Exception as error:
#         print("Connecting to database failed.")
#         print("Error: ", error)
#         time.sleep(2)
