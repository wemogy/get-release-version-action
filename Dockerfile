FROM python:3.13-slim

# Install git
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y git && \
    apt clean -y && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.2 /uv /bin/

# Do not update the lock file
ARG UV_FROZEN=1
# Copy cached packages instead of linking them
ARG UV_LINK_MODE=copy
# Compile Python bytecode on build time to improve startup times
ARG UV_COMPILE_BYTECODE=1

# Install dependencies
WORKDIR /app
COPY .python-version pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --no-install-project --no-dev

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy and install source code
COPY src/get_release_version_action/ src/get_release_version_action/
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --no-dev

RUN chmod +x /app/src/get_release_version_action/entrypoint.sh
ENTRYPOINT ["/app/src/get_release_version_action/entrypoint.sh"]
