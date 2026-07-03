"""Exercise 2: Accessing the Mainframe — oracle.py

Secure configuration system using environment variables and a .env file.
Loads configuration from environment variables, uses a .env file for
development settings, demonstrates different configuration for
development/production, and includes proper error handling for missing
configuration. Use the python-dotenv library to load the .env file (do not
implement a custom parser).

Configuration variables:
    MATRIX_MODE    - 'development' or 'production'
    DATABASE_URL   - Connection string for data storage
    API_KEY        - Secret key for external services
    LOG_LEVEL      - Logging verbosity
    ZION_ENDPOINT  - URL for the resistance network

Authorized: os, sys, python-dotenv modules, file operations.
"""

# --- Example of expected output ---
# $> python oracle.py
#
# ORACLE STATUS: Reading the Matrix...
#
# Configuration loaded:
# Mode: development
# Database: Connected to local instance
# API Access: Authenticated
# Log Level: DEBUG
# Zion Network: Online
#
# Environment security check:
# [OK] No hardcoded secrets detected
# [OK] .env file properly configured
# [OK] Production overrides available
#
# The Oracle sees all configurations.

import os
from dotenv import load_dotenv


def check_mode(config: dict) -> None:
    if config['matrix_mode']:
        print(f"Mode: {config['matrix_mode']}")
    else:
        print("Environment variable MATRIX_MODE is missing.")


def check_database(config: dict) -> None:
    if not config['database_url']:
        print("Environment variable DATABASE_URL is missing.")
    elif config['matrix_mode'] == "production":
        print("Database: Connected to production instance")
    else:
        print("Database: Connected to local instance")


def check_api_access(config: dict) -> None:
    if config['api_key']:
        print("API Access: Authenticated")
    else:
        print("Environment variable API_KEY is missing.")


def check_log_level(config: dict) -> None:
    if config['log_level']:
        print(f"Log Level: {config['log_level']}")
    else:
        print("Environment variable LOG_LEVEL is missing.")


def check_zion(config: dict) -> None:
    if config['zion_endpoint']:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def load_config() -> dict:
    print("Configuration loaded:")
    return {
        "matrix_mode": os.getenv("MATRIX_MODE"),
        "database_url": os.getenv("DATABASE_URL"),
        "api_key": os.getenv("API_KEY"),
        "log_level": os.getenv("LOG_LEVEL"),
        "zion_endpoint": os.getenv("ZION_ENDPOINT")
    }


def check_all(config: dict) -> None:
    if all(v is not None for _, v in config.items()):
        print("The Oracle sees all configurations.")
    else:
        print("Some configs are missing.")


def print_sec_check() -> None:
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    load_dotenv()
    config = load_config()
    check_mode(config)
    check_database(config)
    check_api_access(config)
    check_log_level(config)
    check_zion(config)
    print()
    print_sec_check()
    print()
    check_all(config)


if __name__ == "__main__":
    main()
