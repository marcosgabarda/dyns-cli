# `dyns` DNS Updater

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

This will add `dyns` command to your shell:

```bash
$ dyns -h

usage: dyns [-h] [--version] [-v] [--check] [record]

A simple command to update a DNS record in DigitalOcean with your public IP.

positional arguments:
  record      domain name (ex. 'home.example.com') to update with your public IP

options:
  -h, --help  show this help message and exit
  --version   show version
  -v          increase verbosity of the output
  --check     checks the status of the record
```
