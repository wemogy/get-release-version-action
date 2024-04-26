FROM python:3.12-slim

# Install poetry
# Thanks to Soof Golan and jjmerelo from StackOverflow: https://stackoverflow.com/a/72465422
ARG POETRY_VERSION=1.8.2
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Create a venv and install Poetry there
RUN /usr/local/bin/python3.12 -m venv $POETRY_VENV
RUN $POETRY_VENV/bin/python -m pip install -U pip setuptools
RUN $POETRY_VENV/bin/python -m pip install poetry==${POETRY_VERSION}

# Add Poetry to the PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Print which git
RUN echo "which git: $(which git)"

# Install git
RUN apt-get -yq update && \
    apt-get -yq install git && \
    rm -rf /var/lib/apt/lists/*

# Copy the action
COPY ["poetry.lock", "pyproject.toml", "/action/"]
COPY ["get_release_version_action/", "/action/get_release_version_action/"]

# Install dependencies
RUN poetry -C /action install --no-interaction --no-cache --without dev
RUN poetry -C /action install --no-interaction --no-cache --only-root

ENV PYTHONPATH="/action"

RUN chmod +x /action/get_release_version_action/entrypoint.sh
ENTRYPOINT ["/action/get_release_version_action/entrypoint.sh"]
