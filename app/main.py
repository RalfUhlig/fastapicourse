# For running this as a webserver, install package uvicorn, open a console and run
# venv\Scripts\uvicorn.exe app.main:app --reload
# main:     The name of the Python file to start
# app:      The name of the defined FastAPI app
# --reload: Reload the server automatically when the code changes
# Documentation: Get with http://localhost:8000/docs

from fastapi import FastAPI

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=22633s
# Split up the routes in different FastAPI routers.
from .routers import post, user, auth, vote
# Import the configuration.
# https://youtu.be/0sOvCWFmrtA?t=33055
# from .config import settings

# Import handling of CORS
# # https://www.youtube.com/watch?v=0sOvCWFmrtA&t=40468s
from fastapi.middleware.cors import CORSMiddleware

# Setup the database.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=40430s
# Switch of the database setup by sqlalchemy. It's done now by alembic.
# models.Base.metadata.create_all(bind=database.engine)

# Define a FastAPI application.
app = FastAPI()

# Define the origins for CORS
# Allow requests from only own domain.
# origins = []
# Allow requests from Google and YouTube.
# origins = ["https://www.google.com", "https://www.youtube.com"]
# Allow requests from everywhere.
origins = ["*"]

# Configure COORS
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=40468s
app.add_middleware(          # middleware: function that runs before every request.
    CORSMiddleware,
    allow_origins=origins,   # Which domains are allowed to do requests.
    allow_credentials=True,  #
    allow_methods=["*"],     # Which request methods are allowed to be used.
    allow_headers=["*"]      # Which headers are allowed.
)


# Include routers.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}   # Will be converted to JSON.

# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=27764s
# Postman features
#
#  Environments
#    Variables to use in requests
#    Open Environment
#    Create variables
#    On workspace select environment (upper right)
#    Use variables ({{variable}})
#
#  Renew tokens in all requests when logging in
#    When logging in, set an environment variable with the token.
#    Select Tests tab.
#    Choose snippet "Set an environment variable".
#    Use this variable in authentication.

# Query parameters
# Better: Request parameters
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=31112s
# Optional parameters with the request for filtering or sorting the result.

# Environment variables
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=32033s
# It's not good a practice to put urls, credentials and so on
# into the code. The credentials are exposed and changing
# the configuration for productions, the program code had to
# be changed.
# That is the use of environment variables. It's a variable
# configured on the computer.
# On the command line a environment variable is accessed by
# %variable_name%
# In Python it's with
# import os
# value = os.getenv(variable_name)
# Use the windows search to find the configuration for
# environment variables. Configure there as user variables:
# But there are too many issues, especially on Windows, e.g.
# a terminal cannot access environment variables without being
# restarted.
# Better wav:

# Environment file
# File named .env
# There should be a way to check if all necessary environment variables
# are set and have the correct type. One way is to use a pydantic schema
# to do that.
# https://youtu.be/0sOvCWFmrtA?t=32740

# Votes/Likes
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=33680s
# Users should be able to like a post.
# Users should only be to like a post once.
# Retrieving posts should also fetch the total number of likes.
# New table for votes
# Column referencing the post id.
# Column referencing the id of the user who liked the post.
# A user should only be able to like a post once so this means
# we need to ensure every post_id/voter_id is a unique combination.
# Can be done with a primary key that spans multiple columns.
# Primary keys must be unique, so that will fulfill the requirement.

# Database migration tool
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=37818s
# sqlalchemy cannot modify existing database tables. It can only create all
# tables from scratch. That is the limitation of sqlalchemy. But dropping
# all tables just for a change is no way.
# Database migration tools allows to incrementally track changes to database
# schema and rollback changes to any point in time.

# Alembic
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=38025s
# It is a database migration tool
# Can do incremental changes to the database.
# Can automatically pull database models from sqlalchemy and generate
# the proper tables.
# Alembic is a python library.
#
# Install alembic: pip install alembic
# Initialize alembic (with directory alembic): alembic init alembic
# In the file alembic.ini, the sqlalchemy.url needs to be set to the database
# connection string. But to use the vales from settings, the value of
# sqlalchemy.url should be overridden from the file alembic\env.py
#
# Edit file alembic\env.py:
#    Add import of Base from models.py to access the models (from app.models import Base)
#    Add import the Setting from config (from app.config import settings)
#    Replace target_metadata = None
#         by target_metadata = Base.metadata
#    After config = context.config add
#
# https://youtu.be/0sOvCWFmrtA?t=38641
# Create a new revision (track the changes): alembic revision -m "Create posts table"
# Open the creates revision file in the directory alembic\versions.
# Edit the upgrade method and add the logic to create everything for this revision.
# Edit the downgrade method and add the logic to go back to the revision before.
# See alembic documentation, chapter "DDL Internals", for details.
# Upgrade to a specific revision: alembic upgrade revision_identifier
# Upgrade the newest revision: alembic upgrade head
# Upgrade one revision (next revision): alembic downgrade +1
# Get the current alembic revision: alembic current
# Downgrade to a specific revision: alembic downgrade revision_identifier
# Downgrade one revision (revision before): alembic downgrade -1
# Generate a revision according to the sqlalchemy models, that are defined: alembic revision --autogenerate -m "message"
# So it's possible to just add changes to the sqlalchemy models and let alembic create the
# necessary logic in a revision automatically.

# What is the CORS policy?
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=40468s
# CORS = Cross Origin Resource Sharing
# Allows to make requests from a web browser on one domain to
# a server on a different domain.
# By default, the API created with FastAPI will only allow
# web browsers running on th same domain as our server to make
# requests to it.
# To allow access from other domains:
#    from fastapi.middleware.cors import CORSMiddleware
#    app.add.middleware(
#        CORSMiddleware,
#        allow_origin=origins,
#        allow_credentials=True,
#        allow_methods=["*"],
#        allow_headers=["*"]
#    )

# GIT
# Preparations
#   Create file .gitignore and add
#     __pycache__
#     venv/
#     .env
#
#   Create a file with all installed libraries
#     pip freeze > requirements.txt
#   To install all libraries from this file:
#     pip install -r requirements.txt
#
# Install git
#   Download the latest version from https://git.org and install it.
# Upgrade git to a newer version: In a console:
#   git update-git-for-windows
#
# Create a project on git
# Create a repository.
#    git init
#    git add --all
#    git commit -m "Initial commit"
#    git branch -M main
#    git remote add origin https://github.com/RalfUhlig/fastapicourse.git
#    git push -u origin main

# Deploying methods
#
# Deploying to Heroku
#   https://heroku.com
#   Create an account at Heroku: Follow the steps of signing up.
#   Install Heroku CLI: https://devcenter.heroku.com/articles/getting-started-with-python#set-up
#   Check the installation: In a console: heroku --version
#   Create an app: In a console: heroku create fastapicourse
#     The name ahas to be global unique.
#     Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.
#   Creating a Heroku app also sets up a new git remote: To check, in a console: git remote
#   Push the app to Heroku: In a console: git push heroku main
#   URL for the app at Heroku: https://fastapicourse.herokuapp.com/
#   Configure the app at Heroku
#      Create file named Procfile (exactly like that), with content:
#         web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}



