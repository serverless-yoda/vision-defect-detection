# application/dto/defect_result_dto.py

# Importing BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel
from typing import Dict, Any


class DefectResultDTO(BaseModel):
    """
    DefectResultDTO is a Data Transfer Object (DTO) used to represent
    the response payload for defect detection results.

    This class ensures that the data returned to the client is structured,
    validated, and easy to serialize (e.g., to JSON).

    Attributes:
        image_id (str): Unique identifier for the analyzed image.
        is_defective (bool): Indicates whether the image contains a defect.
        probabilities (Dict[str, float]): A dictionary mapping defect categories
                                          to their predicted probabilities.
                                          Example: {"scratch": 0.85, "dent": 0.10}
        notes (Optional[str]): Additional comments or context about the analysis.
    """

    image_id: str  # Unique identifier for the image
    is_defective: bool  # True if a defect was detected, otherwise False
    probabilities: Dict[str, float]  # Defect categories with confidence scores
    notes: str | None = None  # Optional notes or remarks about the result
