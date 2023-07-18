# Python 3.11.4 See https://www.chainguard.dev/unchained/a-guide-on-how-to-use-chainguard-images-for-public-catalog-tier-users for more details on how to update this
FROM cgr.dev/chainguard/python@sha256:bbaba40f4dfff902af5ec49793a8d42478cae07ad9fcd6eace93a55c348a2aa6 

WORKDIR /honeypot-working-dir

COPY . .

# TODO - install Poetry production dependencies via a multistage-build using the dev version of the image

# Arbitrary non-root id, something just below the 65535 limit https://unix.stackexchange.com/questions/191663/any-concerns-with-using-high-uid-numbers-3000-on-rhel5
USER 65532
ENTRYPOINT ["python", "main.py"]