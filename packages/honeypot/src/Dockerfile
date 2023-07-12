FROM cgr.dev/chainguard/python:3.11.4

WORKDIR /honeypot-working-dir

COPY . .

# TODO - install Poetry production dependencies via a multistage-build using the dev version of the image

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT ["python", "main.py"]