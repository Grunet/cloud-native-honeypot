# Adapted from https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/#usage

# Python 3.11.4, dev base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:3b28a1b0635d0dfa88aac767bc9df52807a13d62501b7f77e297e3b97dd84713 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Python 3.11.4, production base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:8a9cfbc08aa85649e8822003fdef85c0eba03c5a138601fd25c1a0c2987382a2 

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY ./src/ .

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT [ "python", "main.py" ]