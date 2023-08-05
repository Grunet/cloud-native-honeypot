FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update

# Honeypot

RUN apt-get install -y python3.11
# This may break ubuntu system packages that are depending on "python" to be of a specific version (e.g. Python 2). For now it seems fine
RUN ln -s /usr/bin/python3.11 /usr/bin/python

RUN wget -O poetryInstallScript.py https://install.python-poetry.org
RUN POETRY_VERSION=1.5.1 POETRY_HOME=/home/vscode/.local/ python poetryInstallScript.py # Poetry relies on $HOME which is /root/ during image build. POETRY_HOME overrides this

# AWS Cloudformation

RUN apt-get install -y python3-pip="22.0.2+dfsg-1ubuntu0.3"
RUN pip install cfn-lint=='0.79.5'

# This is partially duplicated in ci.yaml, with the copy target being the only difference
RUN mkdir ./cfn-guard-temp/
RUN wget https://github.com/aws-cloudformation/cloudformation-guard/releases/download/3.0.0/cfn-guard-v3-ubuntu-latest.tar.gz -O - | tar -xzvf - -C ./cfn-guard-temp/
RUN cp ./cfn-guard-temp/cfn-guard-v3-ubuntu-latest/cfn-guard /home/vscode/.local/bin/
RUN rm -rf ./cfn-guard-temp/