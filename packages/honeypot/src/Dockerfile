FROM cgr.dev/chainguard/python:3.11.4

WORKDIR /honeypot-working-dir

# TODO - add a user

COPY . .

# TODO - install Poetry production dependencies via a multistage-build using the dev version of the image

# TODO - check if this still handles signals correctly
ENTRYPOINT [ "python", "main.py"]