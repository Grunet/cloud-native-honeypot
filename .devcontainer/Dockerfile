FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update
RUN apt-get install -y python3.11
RUN ln -s /usr/bin/python3.11 /usr/bin/python

RUN wget -O poetryInstallScript.py https://install.python-poetry.org
RUN POETRY_VERSION=1.5.1 POETRY_HOME=/home/vscode/.local/ python poetryInstallScript.py # Poetry relies on $HOME which is /root/ during image build. POETRY_HOME overrides this