"""Module with the code to update a DNS record."""

import logging

import httpx
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration of the updater."""

    digital_ocean_token: SecretStr

    model_config = SettingsConfigDict(env_prefix="dyns_")


def public_ip() -> str:
    """Get the public IP of the host.

    It uses https://www.ipify.org/.
    """
    response = httpx.get("https://api.ipify.org?format=json")
    response.raise_for_status()
    data = response.json()
    logger.debug(f"Public IP: {str(data)}")
    return response.json()["ip"]


def updater(name: str, domain: str) -> None:
    """Update the DNS record using the DigitalOcean API."""
    settings = Settings()
    token = settings.digital_ocean_token.get_secret_value()

    base_url = "https://api.digitalocean.com/v2"
    headers = {"Authorization": f"Bearer {token}"}

    # creates a client
    with httpx.Client(base_url=base_url, headers=headers) as do_client:
        # looks for the record ID using the list endpoint
        # ------------------------------------------------------------------------------
        response = do_client.get(f"/domains/{domain}/records")
        response.raise_for_status()

        data = response.json()
        domain_records = data["domain_records"]

        # handle pagination
        next = data["links"]["pages"].get("next")
        while next:
            response = do_client.get(next)
            response.raise_for_status()
            data = response.json()
            domain_records += data["domain_records"]
            next = data["links"]["pages"].get("next")

        # filter the results
        records = [record for record in domain_records if record["name"] == name]
        if not records:
            logger.error(f"Record {name} not found in domain {domain}")
            return None
        record = records[0]

        # updates the record
        # ------------------------------------------------------------------------------

        ip = public_ip()
        payload = {"type": "A", "data": ip}
        response = do_client.patch(
            f"/domains/{domain}/records/{record['id']}", json=payload
        )
        response.raise_for_status()
        logger.info(f"DNS record updated with '{ip}'")
