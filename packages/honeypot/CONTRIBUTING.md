## Honeypot - Contributing

### Code Auto-Formatting

Sometimes the `black` VS Code extension doesn't work on startup of a Codespace. If it doesn't seem to be auto-formatting on save try

1. Disabling the extension
2. Reloading the workspace
3. Re-enabling the extension

That seems to usually fix it.

### Dependency Management

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





TODO - add a callout for this - Codespaces devcontainer version of Python installed via apt-get is pinned down to a minor version, not a patch version (Could pin to a patch version if compiling Python from scratch but this would be very very slow)

TODO - Philosophy is that should try to avoid production PyPi dependencies as much as possible, but taking on more dev dependencies as is convenient is acceptable risk