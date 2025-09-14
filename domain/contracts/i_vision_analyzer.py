# domain/contracts/i_vision_analyzer.py

# Importing Abstract Base Class (ABC) and abstractmethod to define an interface-like class
from abc import ABC, abstractmethod

# Importing DefectResult, which likely represents the result of analyzing an image for defects
from domain.entities.defect_result import DefectResult


class IVisionAnalyzer(ABC):
    """
    IVisionAnalyzer is an abstract base class (interface) that defines the contract
    for any vision analysis component in the system.
    
    Classes implementing this interface must provide an asynchronous method
    to analyze an image and return a DefectResult.
    """

    @abstractmethod
    async def analyze_image(self, image_byte: bytes) -> DefectResult:
        """
        Analyze the given image and return a DefectResult.

        Args:
            image_byte (bytes): The image data in bytes format to be analyzed.

        Returns:
            DefectResult: An object containing the analysis result, such as
                          detected defects, confidence scores, and other metadata.

        Note:
            This method is asynchronous and must be awaited when called.
        """
        pass
