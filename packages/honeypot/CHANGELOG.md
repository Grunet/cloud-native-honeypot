# Changelog

## What constitutes a breaking change?

This package is unique in that the actual behavior of the honeypot servers is not part of the "API surface", meaning that the servers' API surfaces should not be relied on and may change without major version bumps.

What is in scope for breaking changes includes

- Environment variables for the docker image
- Ports exposed by the docker image
- Container healthcheck routes exposed by the docker image
- Metadata and details of published events

## Changes

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