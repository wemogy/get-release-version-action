FROM python:3.12-slim

# importing the action
COPY ["src", "."]

# installing the dependencies
RUN pip install -r requirements.txt

ENV GIT_PYTHON_REFRESH=quiet

# running the action
ENTRYPOINT ["python", "app.py"]

