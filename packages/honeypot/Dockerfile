# Adapted from https://edu.chainguard.dev/chainguard/chainguard-images/reference/python/overview/#usage

# Python 3.11.4, dev base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:ed93b11743a002aa79f7f084d2f23b7040a8c35ce26a34b7918f15db16fbc8f2 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --user

# Python 3.11.4, production base image. See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:bbaba40f4dfff902af5ec49793a8d42478cae07ad9fcd6eace93a55c348a2aa6 

# Make sure you update Python version in path
COPY --from=builder /home/nonroot/.local/lib/python3.11/site-packages /home/nonroot/.local/lib/python3.11/site-packages

COPY ./src/ .

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT [ "python", "main.py" ]