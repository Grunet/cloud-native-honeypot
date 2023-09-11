# Adapted from https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/#usage

# Python 3.11.5, dev base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:e51a0b8de16b38ab18c2571ff8b0d27e6d5ad6285ec80c532dcc9feaa0444ff8 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Python 3.11.5, production base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:c8cbd40534c4db9d7167aec76982a248d2a3c21d42dcb4af411da552708067b3 

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY ./src/ .

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT [ "python", "main.py" ]