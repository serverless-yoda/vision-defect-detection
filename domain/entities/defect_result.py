# domain/entities/defect_result.py

# Importing BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict


class DefectResult(BaseModel):
    """
    DefectResult represents the outcome of analyzing an image for defects.
    This entity is part of the domain layer and is used to transfer structured
    defect detection results across the system.
    """

    image_id: str
    # Unique identifier for the analyzed image (e.g., filename or UUID)

    timestamp: datetime
    # The date and time when the analysis was performed

    is_defective: bool
    # Indicates whether the image contains a defect (True) or not (False)

    probabilities: Dict[str, float]
    # A dictionary mapping defect categories to their predicted probabilities
    # Example: {"scratch": 0.85, "dent": 0.10}

    raw_response: Dict
    # The raw response from the underlying vision model or API
    # Useful for debugging or storing additional metadata

    notes: Optional[str] = None
    # Optional field for adding human-readable comments or extra context
