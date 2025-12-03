"""Module with CLI application."""

import argparse
import json
import logging
import sys

import dyns

from .api import public_ip, retrieve_record, updater

logger = logging.getLogger(__name__)


def update_dns_record(args: argparse.Namespace) -> None:
    """Parse the record and update the DNS record."""
    parts = args.record.split(".")
    domain = ".".join(parts[-2:])
    name = ".".join(parts[:-2])

    if args.check:
        record = retrieve_record(name=name, domain=domain)
        if not record:
            msg = f"Record {name}.{domain} not found"
            logger.error(msg)
            sys.exit(-1)

        print("Record:\n", json.dumps(record, indent=2))
        ip = public_ip()
        print("Public IP:", ip)
        if ip != record["data"]:
            print("\033[91mThe record has to be updated!\033[0m")
        else:
            print("\033[92mThe record is updated!\033[0m")

    else:
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
        nargs="?",
        help="domain name (ex. 'home.example.com') to update with your public IP",
    )
    parser.add_argument("--version", help="show version", action="store_true")
    parser.add_argument(
        "-v", help="increase verbosity of the output", action="store_true"
    )
    parser.add_argument(
        "--check", help="checks the status of the record", action="store_true"
    )
    parser.set_defaults(func=update_dns_record)
    args = parser.parse_args()

    # check verbosity
    if args.v:
        logging.basicConfig(level=logging.INFO)

    # just print version
    if args.version:
        print(dyns.__version__)
        sys.exit(0)
    elif not args.record:
        print("You need to indicate a DNS record to update")
        sys.exit(-1)

    args.func(args)
