# For more information, please refer to https://aka.ms/vscode-docker-python
FROM mcr.microsoft.com/devcontainers/python:latest
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update && apt-get install -y procps
RUN apt-get install -y git
RUN pip install --upgrade pip
RUN pip install -U debugpy
RUN pip install requests
RUN pip install sentence-transformers
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install -r requirements.txt

# RUN mkdir /app
# COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["sleep", "infinity"]
