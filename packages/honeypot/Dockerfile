# Adapted from https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/#usage

# Python 3.11.5, dev base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:2dccbdb82841992fe1ff8413c533036aae3aa6539462ba288c64b66ec3199e27 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Python 3.11.5, production base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:36d9faf5198aec34124b2d8434b23dbe518f72ecc62d51b2b8e29fbd62f44110 

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY ./src/ .

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT [ "python", "main.py" ]