FROM mcr.microsoft.com/devcontainers/base:alpine-3.18

RUN apk add python3=~3.11.4

RUN wget -O poetryInstallScript.py https://install.python-poetry.org
RUN POETRY_VERSION=1.5.1 POETRY_HOME=/home/vscode/.local/ python poetryInstallScript.py # Poetry relies on $HOME which is /root/ during image build. POETRY_HOME overrides this

# Needed for Earthly
RUN apk add podman=~4.5.1
# Needed for podman per https://github.com/containers/buildah/issues/3666#issuecomment-1349687679
RUN apk add fuse-overlayfs
RUN sed -i 's/#mount_program/mount_program/' /etc/containers/storage.conf

# Sudo required per Earthly usage with podman
RUN sudo wget https://github.com/earthly/earthly/releases/download/v0.7.11/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly && /usr/local/bin/earthly bootstrap --with-autocomplete