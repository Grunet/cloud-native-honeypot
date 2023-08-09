# Honeypot - Security

## Supply Chain Security

### Verifying Container Signatures for Tamperment Detection

To verify the container image hasn't been modified post-publishing, follow these steps:

1. [Install cosign](https://docs.sigstore.dev/cosign/installation/) (make sure to update the steps to use the latest version)
2. Get the SHA of the container image (i.e. by clicking into one of the lines in https://github.com/Grunet/cloud-native-honeypot/pkgs/container/cloud-native-honeypot)
3. Run the following command

```bash
cosign verify --certificate-oidc-issuer=https://token.actions.githubusercontent.com --certificate-identity=https://github.com/Grunet/cloud-native-honeypot/.github/workflows/release-honeypot.yaml@refs/heads/main ghcr.io/grunet/cloud-native-honeypot@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Where the long string of a's is replaced by the actual SHA.

You should then see output like 

```
Verification for ghcr.io/grunet/cloud-native-honeypot@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The code-signing certificate was verified using trusted certificate authority certificates
```

which confirms the repository and image haven't been tampered with.

### Notes on Github Workflows

Python installs should be cached in CI according to https://github.com/actions/setup-python/blob/main/docs/advanced-usage.md#hosted-tool-cache

Pypi poetry dependencies should be cached by the `setup-python` action in CI.

Docker layers should be getting cached in Github Actions per the settings on the docker/build-push-action action (specifically the `mode=max`) that should be aggressively caching intermediate layers of the multi-stage build (and not just the final layer). This should mean that dependencies should be getting pulled from cache, so long as the requirements.txt file doesn’t change (or anything prior in the Dockerfile to the installing of dependencies with pip that would trigger subsequent layer caches to be invalidated) rather than redownloaded from the internet.

## Tools in Place

### Security Static Analysis

Github's CodeQL enabled at the repository level with the default configuration is the only thing currently in use for the Python code in this subproject.