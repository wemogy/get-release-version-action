FROM python:3.12-slim

# importing the action
COPY ["src", "/action"]

# installing the dependencies
RUN pip install -r /action/requirements.txt

# Print which git
RUN which git

# Install git
RUN apt-get -yq update && apt-get -yq install git && rm -rf /var/lib/apt/lists/*

RUN chmod +x /action/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/action/entrypoint.sh"]
