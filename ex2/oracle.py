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
