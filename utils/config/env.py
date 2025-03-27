import os
import json
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
from utils.config.logger import logger


# Load environment variables for local development
if os.getenv("ENVIRONMENT") is None:
    load_dotenv()

# Retrieve Key Vault details from environment
KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME")
if not KEY_VAULT_NAME:
    logger.error("KEY_VAULT_NAME environment variable is not set.")
    raise ValueError("KEY_VAULT_NAME environment variable is required.")
KV_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net/"

# Initialize Azure credentials
try:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KV_URL, credential=credential)
    logger.info("Azure credentials initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Azure credentials: {e}")
    raise

# Global dictionary to store secrets
secrets_cache = {}


def get_secret(secret_name: str) -> str:
    """
    Retrieve a secret from the cache or Azure Key Vault with error handling.
    """
    # Check if secret is already cached
    if secret_name in secrets_cache:
        logger.info(f"Secret '{secret_name}' found in cache.")
        return secrets_cache[secret_name]
    try:
        # Secret not in cache, retrieve from Azure Key Vault
        secret = client.get_secret(secret_name)
        # secrets_cache[secret_name] = secret.value # Cache the secret
        response = json.loads(secret.value)
        for param in response:
            secrets_cache.update(param)
        logger.info(f"Successfully retrieved and cached secret: {secret_name}")
        return secret.value
    except Exception as e:
        logger.error(f"Error retrieving secret '{secret_name}': {e}")
        return None


def load_all_secrets():
    """
    Check if the secrets cache is empty, and if so, load all required secrets.
    """
    if not secrets_cache:
        logger.info("Secrets cache is empty. Retrieving secrets from Azure Key Vault.")
        # Retrieve secrets (for example, "MY_SECRET_KEY")
        MY_SECRET_KEY = get_secret(os.getenv("MY_SECRET_KEY"))
        if MY_SECRET_KEY:
            os.environ["MY_SECRET_KEY"] = MY_SECRET_KEY
            logger.info("MY_SECRET_KEY set in environment variables.")
        else:
            logger.error("Failed to retrieve MY_SECRET_KEY from Azure Key Vault.")


# Call the load_all_secrets function to load secrets at the beginning
load_all_secrets()


# workflow
VERIFY_CHECK = secrets_cache["VERIFY_CHECK"]
MAX_RETRY = int(secrets_cache["MAX_RETRY"])
PDF_LENGTH_RANGE = int(secrets_cache["PDF_LENGTH_RANGE"])
FUZZY_THRESHOLD = int(secrets_cache["FUZZY_THRESHOLD"])

# azure form recognizer credentials
API_VERSION = secrets_cache["API_VERSION"]
MODEL_NAME = secrets_cache["MODEL_NAME"]
AZURE_FORM_RECOGNISER_ENDPOINT = secrets_cache["AZURE_FORM_RECOGNISER_ENDPOINT"]
MODEL_ID = secrets_cache["MODEL_ID"]
FORM_RECOGNITION_SUBSCRIPTION_KEY = secrets_cache["FORM_RECOGNITION_SUBSCRIPTION_KEY"]

# azure open-ai
AZURE_REGION = secrets_cache["AZURE_REGION"]
AZURE_OPENAI_VERSION = secrets_cache["AZURE_OPENAI_VERSION"]
AZURE_ENDPOINT = secrets_cache["AZURE_ENDPOINT"]
AZURE_API_KEY = secrets_cache["AZURE_API_KEY"]
DEPLOYMENT_NAME = secrets_cache["DEPLOYMENT_NAME"]

# database credentials
DB_HOST = secrets_cache["HOST"]
DB_PORT = int(secrets_cache["PORT"])
DB_USERNAME = secrets_cache["USERNAME"]
DB_PASSWORD = secrets_cache["PASSWORD"]
DB_DATABASE_NAME = secrets_cache["DATABASE_NAME"]

# azure blob
CONNECTION_STRING = secrets_cache["CONNECTION_STRING"]
CONTAINER_NAME = secrets_cache["CONTAINER_NAME"]
ARCHIVED_CONTAINER_NAME = secrets_cache["ARCHIVED_CONTAINER_NAME"]

# Number of days for archived emails
ARCHIVE_EMAIL_DAYS = int(secrets_cache["ARCHIVE_EMAIL_DAYS"])


# Service principal
SECRET_KEY = secrets_cache["SECRET_KEY"]
ALGORITHM = secrets_cache["ALGORITHM"]

# Duck-creek
DC_USERNAME = secrets_cache["DC_USERNAME"]
DC_PASSWORD = secrets_cache["DC_PASSWORD"]

# o-auth-cred
AZURE_CLIENT_ID = secrets_cache["AZURE_CLIENT_ID"]
AZURE_TENANT_ID = secrets_cache["AZURE_TENANT_ID"]
AZURE_CLIENT_SECRET = secrets_cache["AZURE_CLIENT_SECRET"]

# Mail-box
OUTLOOK_USER = secrets_cache["OUTLOOK_USER"]

# scheduler
SUPPORT_MAIL_TIME_HRS = int(secrets_cache["SUPPORT_MAIL_TIME_HRS"])
SUPPORT_MAIL_FLAG = bool(secrets_cache["SUPPORT_MAIL_FLAG"])
SUPPORT_MAIL_BOX = secrets_cache["SUPPORT_MAIL_BOX"]
SUPPORT_MAIL_TRIGGER_TIME_MIN = int(secrets_cache["SUPPORT_MAIL_TRIGGER_TIME_MIN"])
