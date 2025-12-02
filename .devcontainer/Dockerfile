# Use Python 3.12 base image
FROM mcr.microsoft.com/devcontainers/python:3.12

ENV PYTHONUNBUFFERED=1

# update the existing packages and install curl
RUN sudo apt-get update && \  
    sudo apt-get install -y curl

# upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH=/root/.local/bin:$PATH