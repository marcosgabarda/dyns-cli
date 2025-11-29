"""Module with CLI application."""

import argparse
import logging
import sys

import dyns

from .updater import updater

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def update_dns_record(args: argparse.Namespace) -> None:
    """Parse the record and update the DNS record."""
    parts = args.record.split(".")
    domain = ".".join(parts[-2:])
    name = ".".join(parts[:-2])
    logger.debug(f"Updating for name {name} in domain {domain}")

    updater(name=name, domain=domain)


def main():
    """Execute main function to handle CLI parameters."""
    parser = argparse.ArgumentParser(
        description=(
            "A simple command to update a DNS record in DigitalOcean with your public "
            "IP."
        )
    )
    parser.add_argument(
        "record",
        type=str,
        help="domain name (ex. 'home.example.com') to update with your public IP",
    )
    parser.add_argument("-v", "--version", help="show version", action="store_true")
    parser.set_defaults(func=update_dns_record)
    args = parser.parse_args()

    # just print version
    if args.version:
        print(dyns.__version__)
        sys.exit(0)

    args.func(args)
