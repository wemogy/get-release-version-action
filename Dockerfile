FROM python:3.12-slim

# importing the action
COPY ["src", "/action"]

# installing the dependencies
RUN pip install -r /action/requirements.txt

# Install git if not installed
RUN which git || ((apt-get -yq update && apt-get -yq install git && rm -rf /var/lib/apt/lists/*) || (apk update --no-cache && apk add --no-cache git))

# running the action
ENTRYPOINT ["python", "/action/app.py"]

