# Honeypot - Contributing

## Dev Environment Quirks

### Code Auto-Formatting

Sometimes the `black` VS Code extension doesn't work on startup of a Codespace. If it doesn't seem to be auto-formatting on save try

1. Disabling the extension
2. Reloading the workspace
3. Re-enabling the extension

That seems to usually fix it.

### Python Version

Codespace's version of Python installed with apt-get is pinned down to a minor version, but not necessarily the same patch version that's in use elsewhere.

It could be pinned to a patch version in `devcontainer.json` but then Python would have to be compiled from scratch, which is very, very slow.

## Dependency Management

### Philosophy of Taking on Dependencies

By default, this project should try to avoid taking on production PyPi dependencies as much as possible, for the sake of runtime security, supply chain security, and maintenance.

Taking on dev PyPi dependencies is more of an acceptable risk by comparison.

### Mechanics of Adding or Updating Dependencies

When adding a new pypi dependency, first add it to Poetry like 

```
poetry add (--dev) <name-of-dependency>
```

Then regenerate `requirements.txt` from the Poetry lockfile like

```
poetry export -f requirements.txt --output requirements.txt
```

This will make sure it's included in the Docker image build (requirements.txt) as well as the local dev environment (Poetry).

The same pattern should be used when updating any pypi dependencies as well.