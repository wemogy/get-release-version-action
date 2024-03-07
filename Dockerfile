FROM python:3.12-slim

# importing the action
COPY ["src", "/action"]

# installing the dependencies
RUN pip install -r /action/requirements.txt

ENV GIT_PYTHON_REFRESH=quiet

# running the action
ENTRYPOINT ["python", "/action/app.py"]

