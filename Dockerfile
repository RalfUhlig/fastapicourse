# Get the base image
FROM python:3.10-buster
# Set a work directory (optional)
WORKDIR /usr/src/app
# Copy the list of requirements to the docker image
COPY requirements.txt ./
# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt
# Copy everything from the current directory to the image.
COPY . .
# Define what to run when the container is started.
# Spaces have to be replaced by separate list items.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
