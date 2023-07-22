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

On a monthly basis, I will check to see if any area is not hitting its target and attempt to rectify that

#### Ubuntu

To find if there's a new LTS version available

1. Navigate to https://wiki.ubuntu.com/Releases
2. Search for the latest release that has "LTS" in the name
    - If the version is the same as the one in use in the repo, there's nothing to do this time
    - If the version is different, continue on

Now that you've found the new Ubuntu LTS version, you'll need to try and update it in these locations

- .devcontainer/Dockerfile
- All files underneath .github/workflows/

If any one of them doesn't yet have support for the new version, there's nothing to do this time.

If they all have it, then create a PR to

1. Update each one
2. Update the changelog and cut a release

#### Python

To find if there's a new minor version available

1. Navigate to https://www.python.org/downloads/source/
2. Find the "Stable Releases"
3. Search for the next minor version after the one in use in the repo (e.g. if the repo is using 3.11 search for 3.12)
    - If you don't find it, there's nothing to do this time
    - If you do find it, continue on

Now that you've found the new Python minor version, you'll need to try and update it in these locations

- .devcontainer/Dockerfile
- .github/workflow/ci.yaml
- packages/honeypot/Dockerfile (implicit in the base images as well as listed in commands)

If any one of them doesn't yet have support for the new version, there's nothing to do this time.

If they all have it, then create a PR to

1. Update each one
2. Update the minimum Python version in packages/honeypot/pyproject.toml
3. Update the changelog and cut a release

### Learning About and Taking Security Patches

TODO