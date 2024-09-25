from dotenv import load_dotenv
import os
from logging_setup import LOGGER
from pathlib import Path

load_dotenv(dotenv_path=".env")

# LOCALV6_PREFIX has the first four hextet
defaults = {
    "LOCALV4": "xxx:xxx:xxx:xxx",
    "LOCALV6_PREFIX": "xxx:xxx:xxx:xxx",
    "GATEWAY_IPV4": "xxx:xxx:xxx:xxx",
    "GATEWAY_IPV6": "xxx:xxx:xxx:xxx:xxx:xxx",
}

# Fetch environment variables with defaults
ip_config = {
    "LOCALV4": os.getenv("LOCALV4", defaults["LOCALV4"]),
    "LOCALV6_PREFIX": os.getenv("LOCALV6_PREFIX", defaults["LOCALV6_PREFIX"]),
    "GATEWAY_IPV4": os.getenv("GATEWAY_IPV4", defaults["GATEWAY_IPV4"]),
    "GATEWAY_IPV6": os.getenv("GATEWAY_IPV6", defaults["GATEWAY_IPV6"]),
}


# Warn missing .env file
if not Path(".env").exists():
    LOGGER.warning("Missing .env IP config. Local IPs will not be masked.")
else:
    # Warn missing individual ip config
    for var, value in ip_config.items():
        if value == defaults[var]:
            LOGGER.warning(f"{var} is not set in the .env file")
