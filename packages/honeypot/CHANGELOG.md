# Changelog

## What constitutes a breaking change?

This package is unique in that the actual behavior of the honeypot servers is not part of the "API surface", meaning that the servers' API surfaces should not be relied on and may change without major version bumps.

What is in scope for breaking changes includes

- Environment variables for the docker image
- Ports exposed by the docker image
- Container healthcheck routes exposed by the docker image
- Metadata and details of published events

## Changes

### v0.4.7

- Update version of Python in CI to 3.11.5

### v0.4.6

- Update Chainguard base images in the Dockerfile
- Add steps in update process to check Chainguard base image signatures

### v0.4.5

- Update Chainguard base images in the Dockerfile

### v0.4.4

- Update Chainguard base images in the Dockerfile

- Re-install moto (dev dependencies) to fix vulnerability alerts about 2 of its direct/transitive dependencies (certifi, cryptography)
- Update Docker version used locally (Codespaces) and CI (Github Workflows)

### v0.4.3

- Keep log lines onto 1 single line (i.e. don't pretty print them) so they match what Fargate's expecting

### v0.4.2

- Update Chainguard base images in the Dockerfile

### v0.4.1

- Update Chainguard base images in the Dockerfile
- Make the logger no-op on exceptions
- Document maintenance and security patching strategy

### v0.4.0

- Add a health check route to the simple http server that doesn't publish an event to Eventbridge
- Standardize almost all logging behind a logger
- Update all code to follow PEP naming conventions for variables and functions (snake_case)
- Update Github releases to point out the changelog

### v0.3.0

- Updated the simple http server to publish an event to an Eventbridge event bus on all GET requests, if the functionality is enabled (via environment variables)

### v0.2.3

- Try fix an issue with cosign prompting in the release workflow
- Update URL in the Github Release to point directly to the container image in Github Packages

### v0.2.2

- Try fix another issue with the casing of the docker tag in the release workflow

### v0.2.1

- Try fix issue with docker tag in release workflow

### v0.2.0

- Create a release workflow for the docker image in Github Actions

### v0.1.0

- Created a simple http server in a docker image behind a ENABLE_SERVER_SIMPLE_HTTP environment variable
