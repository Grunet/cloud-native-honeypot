# Honeypot

## Contributing

### Dependency Management

When adding a new pypi dependency, first add it to Poetry like 

```
poetry add (--dev) <name-of-dependency>
```

Then regenerate `requirements.txt` from the Poetry lockfile like

```
poetry export -f requirements.txt --output requirements.txt
```

This will make sure it's included in the Docker image build (requirements.txt) as well as the local dev environment (Poetry).

The same pattern should be used when updating any pypi dependencies as well.

## Dependency Maintenance

This goes over the maintenance needs and strategies for this subproject.

### Maintenance Needs

The following is an overview of all the areas that may need patches and updates:

- Devcontainer
    - Ubuntu base image version
    - Python version
    - Poetry version
    - Docker-in-Docker feature version
    - Docker version
- Github Workflows
    - Ubuntu runner versions
    - 3rd party action versions
    - Poetry version
    - Python version
    - Docker version
    - Version of binaries (e.g. cosign, curl, jq)
- This Package's Contents
    - Python version (in pyproject.toml)
    - Pypi dependencies
    - Chainguard base images
    - Python version (in Dockerfile)
    - Docker Compose version

### Maintenance Targets

By default, the target for each area is

- Be on the latest major version that has been out for a while

with the exceptions being

- Python (latest minor version for Python 3 is the equivalent)
- Well-known binaries (e.g. curl, jq, that don't strictly need their versions pinned as much)
- Docker Compose version (latest minor version is the equivalent)

The goals here are twofold

- To stay away from end-of-life and lack of security support situations
- To always be able to easily uptake security patches without needing to worry about breaking changes at the same time

### Maintenance Strategy

TODO

### Learning About and Taking Security Patches

TODO