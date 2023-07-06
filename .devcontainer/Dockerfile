FROM mcr.microsoft.com/devcontainers/base:alpine

RUN apk add python3=~3.11.4

RUN wget -O poetryInstallScript.py https://install.python-poetry.org
RUN POETRY_HOME=/home/vscode/.local/ python poetryInstallScript.py # Poetry relies on $HOME which is /root/ during image build. POETRY_HOME overrides this