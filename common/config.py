# common/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings class for managing application configuration using environment variables.

    Attributes:
        app_name (str): Name of the application.
        azure_key_vault_name (str): Name of the Azure Key Vault.
        azure_cognitive_api_key (str): Secret name or value for the Azure Cognitive Services API key.
        azure_cognitive_endpoint_url (str): Secret name or value for the Azure Cognitive Services endpoint URL.
    """

    # Application name
    app_name: str = "Azure Vision Defect Detection"

    # Azure Key Vault and Cognitive Services configuration
    azure_key_vault_name: str
    azure_cognitive_api_key: str
    azure_cognitive_endpoint_url: str

    class Config:
        # Specify the name of the environment file and encoding to load variables from
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate the settings object to be used throughout the application
settings = Settings()
