FROM python:3.12-slim

# importing the action
COPY ["src", "/action"]

# installing the dependencies
RUN pip install -r /action/requirements.txt

# Install git
RUN apk update --no-cache && apk add --no-cache git

RUN chmod +x /action/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/action/entrypoint.sh"]
