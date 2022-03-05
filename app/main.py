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
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41018s
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
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41260s
#   Download the latest version from https://git.org and install it.
# Upgrade git to a newer version: In a console:
#   git update-git-for-windows
#
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41363s
# Create a project on github
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
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41679s
#   https://heroku.com
#   Create an account at Heroku: Follow the steps of signing up.
#   Install Heroku CLI: https://devcenter.heroku.com/articles/getting-started-with-python#set-up
#   Check the installation: In a console: heroku --version
#   https://www.youtube.com/watch?v=0sOvCWFmrtA&t=41740s
#   Create an app: In a console: heroku create fastapicourse
#     The name ahas to be global unique.
#     Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.
#   Creating a Heroku app also sets up a new git remote: To check, in a console: git remote
#   Push the app to Heroku: In a console: git push heroku main
#   Status of the app can be monitored in the Heroku dashboard.
#   URL for the app at Heroku: https://fastapicourse.herokuapp.com/
#   Show the error log: In a console: heroku logs --tail
#   Configure the app at Heroku
#   https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42021s
#      Create file named Procfile (exactly like that), with content:
#         web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
#   Add the file to git and push to Heroku. In a console
#     git add --all
#     git commit -m "..."
#     git push heroku main
#   Add a database
#   https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42299s
#      Install MariaDB as addon: In a console: heroku addons:create jawsdb-maria:kitefin    Credit Card needed!
#      Install PostGRES as addon: In a console: heroku addons:create heroku-postgresql:hobby-dev
#      Status of the database can be monitored in the Heroku dashboard.
#      Under the app, database, setting, the credentials can be seen.
#   Set environment variables
#   https://www.youtube.com/watch?v=0sOvCWFmrtA&t=42522s
#      Under the app, settings, reveal config vars, the environment variables can be configured.
#      The database URL should already be configured.
#      Set all the needed variables.
#         DATABASE_CONNECTOR=postgresql
#         DATABASE_HOSTNAME=
#         DATABASE_PORT=
#         DATABASE_USERNAME=
#         DATABASE_PASSWORD=
#         DATABASE_NAME=
#         SECRET_KEY="xxx"
#         SIGNING_ALGORITHM=HS256
#         ACCESS_TOKEN_EXPIRE_MINUTES=60
#   Restart the heroku app: In a console: heroku ps:restart
#   Show the error log: In a console: heroku logs --tail
#   Create database structure
#   https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43139s
#      Use the alembic revisions to create the database structure at Heroku.
#      All alembic revisions are check in, so they are also at Heroku.
#      In a console: heroku run "alembic upgrade head"
#   Restart the heroku app: In a console: heroku ps:restart
#   Show the error log: In a console: heroku logs --tail
#
# Deploy on Ubuntu VM (here it's done with RasbianOS 11)
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43504s
# Install RasbianOS 11 on Raspberry Pi 4
# Update packages
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43684s
#   sudo apt update
#   sudo apt
# Install git
#    sudo apt install git
# Install Python
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43847s
#   sudo apt install python3-pip
# Install virtualenv
#   sudo pip install virtualenv
# Install Postgres
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=43941s
#   sudo apt install postgresql postgresql-contrib
# Configure postgres
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=44248s
# By default postgres is using peer authentication (sometimes named integrated authentication).
# That means, that the connection is always done with the user that is logged on the machine.
# With the installation of postgres, a system user postgres is created. So the login has to be
# with this user postgres.
#   sudo su - postgres
# Connect to the default database postgres and default user postgres with psql:
#   psql -U postgres
# Set a password for database user postgres (here postgres):
#   \password postgres
# Exit from psql:
#   \q
# Leave user postgres:
#   exit
# Change the postgres configuration to allow access not only from localhost:
#   sudo nano /etc/postgresql/13/main/postgresql.conf
#     Under listen_addresses = 'localhost' add
#     listen_addresses = '*'
# Change the postgres client authentication to allow access with a given user
# and from other computers than localhost:
#   sudo nano /etc/postgresql/13/main/pg_hba.conf
#     In line: local   all             postgres                                peer
#       Change peer by md5
#     In line: local   all             all                                     peer
#       Change peer by md5
#     In line: host    replication     all             127.0.0.1/32            md5
#       Change 127.0.0.1/32 by 0.0.0.0/0
#     In line: host    all             all             ::1/128                 md5
#       Change ::1/128 by ::/0
# Restart postgres
#   sudo systemctl restart postgresql
# Add a new user
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=44690s
#   Create a user: sudo adduser <username>
#   Give a passwort
#   Allow the user to use sudo: sudo usermog -aG sudo <username>
#   Login with this user
# Create a directory for our project
#   mkdir FastAPICourse
#   cd FastAPICourse
# Create a virtual Python environment
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=44690s
#   Create the environment: virtualenv venv
#   Activate the environment: source venv/bin/activate
#   Leave an environment: deactivate
# Create a folder for the source code
#   mkdir src
#   cd src
# Get the project from github
# https://youtu.be/0sOvCWFmrtA?list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&t=44986
#   Clone the project from github without creating another directory
#   with the name of the project:
#     git clone https://github.com/RalfUhlig/fastapicourse.git .
#   Install all requirements
#     pip install -r requirements.txt
#   Try to start the app
# Set environment variables
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=45246s
#   Set an environment variable: export name=value
#   Show all environment variables: printenv
#   Delete an environment variable: unset name
#   Create an empty file named .env: touch .env
#   Fill with necessary variables.
#   Set all variables as exported: set -o allexport; source ~/.env; set +o allexport
#   One way to automatically load the environment variables after booting is to
#   put this command into file .profile at the bottom.
# Setup te database
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=45744s
#   Create the database FastAPICourse
#   Note: In postgres there is no way to see all databases. You always connect to one database
#         and work with it. The database is shown as "public".
#   Create the database structure: alembic upgrade head
# Start the application again, listening on any ip address.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=45957s
#   uvicorn --host 0.0.0.0 app.main:app
# Use process manager to supervise the app.
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=46452s
#   Install gunicorn and its requirements:
#     pip install gunicorn
#     pip install httptools
#     pip install uvloop
#   Update requirements.txt
#   gunicorn allows more than one worker (option -w or --workers)
#   Start app with gunicorn with 4 uvicorn workers listing at any ip address on port 8000:
#     gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app
# Run the app as systemd service
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=46452s
#   Service file: gunicorn.service
#     Description: Description of the service.
#     After: When to start.Here after network is up.
#     User: User to run the service.
#     Group: Group of the user (see /etc/group).
#     WorkingDirectory: Directory the service is running in.
#     Environment: Path to the bin folder for the Python environment.
#     ExecStart: Path to the command to run the service.
#     WantedBy: Running the service when the system starts in multi user mode.
#   Copy gunicorn.service to /etc/systemd/system (as root) as FastAPICourse.service.
#   or edit it by: sudo nano /etc/systemd/system/FastAPICourse.service
#   Note: After editing a service file: sudo systemctl daemon-reload
#   Check the service file: sudo systemctl status FastAPICourse
#   Start the service: sudo systemctl start FastAPICourse
#   Enable automatic restart after reboot: sudo systemctl enable FastAPICourse
# Using NGINX as a high performance proxy
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=47085s
#     High performance webservers can act as a proxy.
#     Can handle SSL termination.
#     HTTPS request ------> NGINX -----> HTTP -----> Gunicorn workers
#     Gunicorn can handle HTTPS too, but it is not optimized for that as NGINX is.
#   Install NGINX: sudo apt install nginx
#   Start NGINX: sudo systemctl start nginx
#   Enable automatic restart after reboot: sudo systemctl enable nginx
#   Configuration of the default page: /etc/nginx/sites-available/default
#   Copy gunicorn.nginx to /etc/nginx/sites-available/FastAPICourse
#   Enable the new site: sudo ln -s /etc/nginx/sites-available/FastAPICourse /etc/nginx/sites-enabled/FastAPICourse
#   Disable the default site: sudo rm /etc/nginx/sites-enabled/default
#   Restart nginx: sudo systemctl restart nginx
#   App now available by http://webservicebox
# Setup a domain name
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=47445s
#   Only works with a domain name, a dns server and the app setup on a public server.
# Setup SSL
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=47719s
#   Lets Encrypt: https://certbot.eff.org/
#   Get Certbot instructions
#   Choose software (nginx) and system (debian 10)
#   Install snapd: sudo apt install snapd
#   Install the snapd core: sudo snap install core
#   Update th snapd core to te newest version: sudo snapd refresh core
#   Install certbot: sudp snap install --classic certbot
#   Configure nginx for using certbot: sudo certbot --nginx
#     Email address needed.
#     Disagree to share the email address.
#     Enter the domain name(s) the certificate is used for.
#   Configuration for default website will be changed.
#   Also a cronjob or a systemd timer is installed for renewing the certificate.
#     Check /etc/crontab/, /etc/cron.*/*, sudo systemctl list-timers
#   Test the automatic renewal: sudo certbot renew --dry-run
# UFW: Uncomplicated Firewall
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=48006s
#    Install ufw: sudo apt install ufw
#    Check status: sudo ufw status
#    Setup firewall rules. The following command create ipv4 as well as an ipv6 rules.
#    from access from anywhere.
#      sudo ufw allow http
#      sudo ufw allow https
#      sudo ufw allow ssh
#      # Allow access to prosgres poer 5432. Not recommended.
#      sudo ufw allow 5432
#    Activate the filrewall
#      sudo ufw enable
#    Remove a rule (e.g. 5432):
#      sudo ufw delete allow 5432
#    Deactivate the firewall
#      sudo ufw disable
# Pushing code changes to production
# https://www.youtube.com/watch?v=0sOvCWFmrtA&list=RDCMUC8butISFwT-Wl7EV0hUK0BQ&index=1&t=48227s
#   # Goto the app directory
#   cd ~/FastAPICourse/src
#   # Pull the latest version from git repository.
#   git pull
#   # Update all requirements
#   pip install -r requirements.txt
#   # Restart the app
#   sudo systemctl restart FastAPICourse
#   Best practice: Setup a CI/CD pipeline
#
# Deploy on Docker
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=48369s
#   To create a custom image, start of with a base image for Python and customize it to copy
#   the source code of the app into it and install all dependencies. That is done with the Dockerfile.
#   Each command in the Dockerfile is a layer. When creating an image all layers are cached. When
#   changes are made, unchanged layers are just copied from the cache. This speeds up the update
#   of an image. So long time taking processes that nearly never changes should be run first.
#   Build the docker image with the Dockerfile in the current directory (tag has to be lowercase):
#     docker build -t fastapicourse .
# Managing docker containers with docker-compose
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=49119s
#   docker-compose is used to spin up the containers automatically
#   Configuration: Filke docker-compose.yml
#   In yml files spacing matters like in Python.
#   For spinning up a container, a service has to be defined.
#     image: Image to create a container to start.
#     build: Builds an image if it does not exist. Parameter is the directory with the Dockerfile.
#            The created image will be named directory_containername_nr, so here fastapi_fastapicourse_1
#     ports: List of ports to open. Format: <post on localhost>:<port on container>
#   Start the configured containers with:
#     docker-compose up --detach
#   Stop and remove all configured containers with:
#     docker-compose down
