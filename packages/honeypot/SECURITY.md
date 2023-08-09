# Honeypot - Security

TODO - document how to install cosign, then pick an image SHA, then run the following command

cosign verify --certificate-oidc-issuer=https://token.actions.githubusercontent.com --certificate-identity=https://github.com/Grunet/cloud-native-honeypot/.github/workflows/release-honeypot.yaml@refs/heads/main ghcr.io/grunet/cloud-native-honeypot@sha256:6282d824407abb0caefec65574cd40ad995a654ae2b24083a46d02fe12e626fb

Then should see 

Verification for ghcr.io/grunet/cloud-native-honeypot@sha256:6282d824407abb0caefec65574cd40ad995a654ae2b24083a46d02fe12e626fb --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The code-signing certificate was verified using trusted certificate authority certificates

TODO - document something about Python install in CI not requiring new downloads per https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#hosted-tool-cache

TODO - document about pypi dependencies being cached in CI

TODO - Docker layers should be getting cached in Github Actions per the settings on the docker/build-push-action action specifically the “mode=max” that should be aggressively caching intermediate layers of the multi-stage build (and not just the final layer). This should mean that dependencies should be getting pulled from cache, so long as the requirements.txt file doesn’t change (or anything prior in the Dockerfile to the installing of dependencies with pip that would trigger subsequent layer caches to be invalidated) rather than redownloaded from the internet

## Tools in Place

## Security Static Analysis

Github's CodeQL enabled at the repository level with the default configuration is the only thing currently in use for the Python code in this subproject.