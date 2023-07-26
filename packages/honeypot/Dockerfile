# Adapted from https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/#usage

# Python 3.11.4, dev base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:b330aa1cd9a0dd5b6f68aad00cb67e8e03f02e6c16eabf9f065a03bb4b2301cd as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Python 3.11.4, production base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:1d681e94835cb783dd717425aa8dff766148bcd6cee0417b8d3a746f0201dd6d 

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY ./src/ .

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT [ "python", "main.py" ]