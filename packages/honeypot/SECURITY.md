# Honeypot - Security

TODO - document something about Python install in CI not requiring new downloads per https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#hosted-tool-cache

TODO - document about pypi dependencies being cached in CI

TODO - Docker layers should be getting cached in Github Actions per the settings on the docker/build-push-action action specifically the “mode=max” that should be aggressively caching intermediate layers of the multi-stage build (and not just the final layer). This should mean that dependencies should be getting pulled from cache, so long as the requirements.txt file doesn’t change (or anything prior in the Dockerfile to the installing of dependencies with pip that would trigger subsequent layer caches to be invalidated) rather than redownloaded from the internet

## Tools in Place

## Security Static Analysis

Github's CodeQL enabled at the repository level with the default configuration is the only thing currently in use for the Python code in this subproject.