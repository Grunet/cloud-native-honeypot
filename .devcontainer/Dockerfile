FROM mcr.microsoft.com/devcontainers/base:alpine

RUN apk add python3=~3.11.4

RUN wget -O poetryInstallScript.py https://install.python-poetry.org
RUN POETRY_VERSION=1.5.1 POETRY_HOME=/home/vscode/.local/ python poetryInstallScript.py # Poetry relies on $HOME which is /root/ during image build. POETRY_HOME overrides this

RUN wget https://github.com/earthly/earthly/releases/v0.7.11/download/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete