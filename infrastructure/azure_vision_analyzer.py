# infrastructure/azure_vision_analyzer.py

import aiohttp, base64, httpx, uuid
from datetime import datetime
from typing import Dict

from domain.contracts.i_vision_analyzer import IVisionAnalyzer
from domain.entities.defect_result import DefectResult
from domain.exceptions import VisionAnalysisError

from common.config import settings
from common.config import get_logger

from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

logger = get_logger(__name__)

class AzureVisionAnalyzer(IVisionAnalyzer):
    """
    AzureVisionAnalyzer uses Azure Cognitive Services to analyze images
    and detect defects based on tags returned by the Computer Vision API.
    """

    def __init__(self):
        """
        Initializes configuration values and placeholders for endpoint, key, and headers.
        """
        # Key Vault and Cognitive Services configuration
        self.key_vault_url = f"https://{settings.azure_key_vault_name}.vault.azure.net/"
        self.azure_cognitive_api_key = settings.azure_cognitive_api_key
        self.azure_cognitive_endpoint_url = settings.azure_cognitive_endpoint_url

        # Placeholders for runtime values
        self.endpoint = None
        self.key = None
        self.url = None
        self.headers = None

    async def initialize(self):
        """
        Asynchronously retrieves secrets from Azure Key Vault and sets up
        the endpoint URL and headers for the Computer Vision API.
        """
        try:
            async with DefaultAzureCredential() as credential:
                async with SecretClient(vault_url=self.key_vault_url, credential=credential) as client:
                    # Retrieve secrets from Key Vault
                    endpoint_secret = await client.get_secret(self.azure_cognitive_endpoint_url)
                    key_secret = await client.get_secret(self.azure_cognitive_api_key)

                    # Set endpoint and key
                    self.endpoint = endpoint_secret.value
                    self.key = key_secret.value

                    # Construct full API URL and headers
                    self.url = f"{self.endpoint.rstrip('/')}/computervision/imageanalysis:analyze?api-version=2023-04-01-preview"
                    self.headers = {
                        "Ocp-Apim-Subscription-Key": self.key,
                        "Content-Type": "application/octet-stream",
                    }
        except Exception as e:
            logger.error(f"Failed to retrieve Key Vault secrets: {e}")
            raise VisionAnalysisError(str(e))

    async def analyze_image(self, image_byte: bytes) -> DefectResult:
        """
        Sends an image to Azure Computer Vision API for analysis and returns
        a DefectResult containing defect status and tag probabilities.

        Args:
            image_byte (bytes): The image data in byte format.

        Returns:
            DefectResult: Contains defect status, tag probabilities, and raw response.
        """
        # Ensure the client is initialized
        if not self.url or not self.headers or not self.endpoint or not self.key:
            raise VisionAnalysisError("Azure Vision analysis client not initialized")

        try:
            # Send image to Azure Vision API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    headers=self.headers,
                    params={"features": "objects,tags"},
                    content=image_byte
                )
                response.raise_for_status()
                payload: Dict = response.json()
        except Exception as e:
            logger.exception("Azure Vision analysis failed")
            raise VisionAnalysisError(str(e))

        # Extract tags containing the word "defect"
        defect_tags = [
            t for t in payload.get("tags", [])
            if "defect" in t["name"].lower()
        ]

        # Determine if the image is defective
        is_defective = len(defect_tags) > 0

        # Map tag names to their confidence scores
        probs = {
            t["name"]: t.get("confidence", 0.0)
            for t in payload.get("tags", [])
        }

        # Return structured result
        return DefectResult(
            image_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            is_defective=is_defective,
            probabilities=probs,
            raw_response=payload
        )
