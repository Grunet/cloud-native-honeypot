# Honeypot

## Contributing

### Code Auto-Formatting

Sometimes the `black` VS Code extension doesn't work on startup of a Codespace. If it doesn't seem to be auto-formatting on save try

1. Disabling the extension
2. Reloading the workspace
3. Re-enabling the extension

That seems to usually fix it.

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

### Maintenance Targets

By default, the target for each area is

- Be on the latest major version that has been out for a while

with the exceptions being

- Python (latest minor version for Python 3 is the equivalent)
- Chainguard base images (staying on the latest images with a compatible Python version)
- Well-known binaries (e.g. curl, jq, that don't strictly need their versions pinned as much)

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
2. Update the changelog, the version, and cut a release

If not, create a Github issue to track it.

#### Python

To find if there's a new minor version available

1. Navigate to https://www.python.org/downloads/source/
2. Find the "Stable Releases"
3. Search for the latest minor version after the one in use in the repo (e.g. if the repo is using 3.11 search for 3.12)
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
3. Update the changelog, the version, and cut a release

If not, create a Github issue to track it.

#### Poetry

To find if there's a new major version available

1. Navigate to https://github.com/python-poetry/poetry/releases
2. Search for the latest major version after the one in use in the repo (e.g. if the repo is using 1.5.1 search for 2.x.y)
    - If you don't find it, there's nothing to do this time
    - If you do find it, continue on

Now that you've found the new major version, you'll need to try and update it in these locations

- .devcontainer/Dockerfile
- .github/workflow/ci.yaml

If any one of them doesn't yet have support for the new version, there's nothing to do this time.

If they all have it, then create a PR to

1. Update each one
2. Re-generate the requirements.txt from the Poetry lockfile
3. Update the changelog, the version, and cut a release

If not, create a Github issue to track it.

#### Docker CLI

To find if there's a new major version available

1. Navigate to https://github.com/moby/moby/releases
2. Search for the latest major version after the one in use in the repo
    - If you don't find it, there's nothing to do this time
    - If you do find it, continue on

Now that you've found the new major version, you'll need to try and update it in these locations

- .devcontainer/devcontainer.json
- .github/workflow/ci.yaml (this may require installing a custom version per https://stackoverflow.com/a/59797984/11866924)

If they all have it available, then create a PR to 

1. Update each one
2. Update the changelog, but don't increment the version nor cut a release yet (since this is a dev-only change)

If not, create a Github issue to track it.

#### Chainguard base images

The first step is to check if the latest Chainguard images contain a newer version of Python. You can figure this out by running the following commands

```bash
docker pull cgr.dev/chainguard/python:latest-dev
docker run --entrypoint sh cgr.dev/chainguard/python:latest-dev -c "python --version"
```

If the version is newer than the one in use, go follow the steps in the [python section above](#python) first.

If the version is the same, that means there's only updates to the rest of the base image to be taken.

Follow these steps to update the base images

1. Navigate to https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/
2. Inspect the date of the latest images releases, and make sure it's not too recent (e.g. the same day)
3. Copy the 2 digests from the page into their corresponding locations in the `Dockerfile`
4. Smoke test the changes by running `make start-docker-simple-http` and `curl http://localhost:8000/`
5. Update the changelog, the version, and cut a release

#### 3rd Party Github Actions

Dependabot should be configured to create monthly PRs for any outdated actions, so just need to review and merge those in.

It should be ignoring all (non-security) patch and minor updates, but in case it isn't this should be controllable on each PR that comes in (there should be an option to make it that way for each particular dependency).

#### Cosign

To find if there's a new major version available

1. Navigate to https://github.com/sigstore/cosign/releases
2. Search for the latest major version after the one in use in the repo (e.g. if the repo is using 2.1.1 search for 3.x.y)
    - If you don't find it, there's nothing to do this time
    - If you do find it, continue on

Now that you've found the new major version, you'll need to try and update it in these locations

- .github/workflow/release-honeypot.yaml

If the action doesn't yet have support for the new version, there's nothing to do this time.

If it does, then create a PR to

1. Update the usage
2. Update the changelog, the version, and cut a release
3. Confirm that the signature continues to show up in Github Packages

If not, create a Github issue to track it.

#### Pypi dependencies

Dependabot should be configured to create monthly PRs for any dependencies out of date by a major version or more.

However, these PRs should just be used as informational-only. The actual updates should be handcrafted in separate PRs (since requirements.txt has to be synchronized)

### Learning About and Taking Security Patches

Picking up security patches requires first learning about them in the first place. These are the strategies for doing that with the dependencies.

#### Python

A watch for releases and security alerts was turned on for https://github.com/python/cpython

#### Poetry

A watch for releases and security alerts was turned on for https://github.com/python-poetry/poetry

#### Docker CLI

A watch for releases and security alerts was turned on for https://github.com/moby/moby

#### Chainguard base images

(Asked about this at https://twitter.com/__grunet/status/1683241030932471808)

#### 3rd Party Github Actions

Dependabot should be creating notices for these.

#### Cosign

A watch for releases and security alerts was turned on for https://github.com/sigstore/cosign

#### Pypi dependencies

Dependabot should be creating notices for these.
