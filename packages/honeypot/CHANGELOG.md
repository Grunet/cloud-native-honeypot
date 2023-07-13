# Changelog

## What constitutes a breaking change?

This package is unique in that the actual behavior of the honeypot servers is not part of the "API surface", meaning that the servers' API surfaces should not be relied on and may change without major version bumps.

What is in scope for breaking changes includes

- Environment variables for the docker image
- Ports exposed by the docker image
- Container healthcheck routes exposed by the docker image

## Changes

### v0.2.1

- Try fix issue with docker tag in release workflow

### v0.2.0

- Create a release workflow for the docker image in Github Actions

### v0.1.0

- Created a simple http server in a docker image behind a ENABLE_SERVER_SIMPLE_HTTP environment variable