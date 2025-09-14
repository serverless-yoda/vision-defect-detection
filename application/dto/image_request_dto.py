# application/dto/image_request_dto.py

# Importing BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel


class ImageRequestDTO(BaseModel):
    """
    ImageRequestDTO is a Data Transfer Object (DTO) used to represent
    the payload for image analysis requests.

    This class ensures that the incoming request data is validated and
    structured properly before being processed by the application.

    Attributes:
        image_base64 (str): The image data encoded as a Base64 string.
                            This is typically sent by the client when
                            uploading an image for analysis.
    """

    image_base64: str  # Base64-encoded image string provided by the client
