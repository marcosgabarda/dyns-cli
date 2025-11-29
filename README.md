# DNS Updater

This small application can be used to update the value of a DNS record in
**DigitalOcean** with the public IP.

This uses [ipify](https://www.ipify.org/) API to obtain the public IP of the host that
executes this application.

## Install

The recommended way to install `dyns` is using [pipx](https://pipx.pypa.io/latest/installation/).
This could be done by using directly the repository URL:

```bash
pipx install git+https://github.com/marcosgabarda/dyns-cli
```

This will add `dyns` command to your shell.
