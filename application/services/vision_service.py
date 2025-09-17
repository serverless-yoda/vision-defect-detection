import base64
from application.dto.defect_result_dto import DefectResultDTO
from application.dto.image_request_dto import ImageRequestDTO
from domain.entities.defect_result import DefectResult
from domain.contracts.i_fabric_repository import IFabricRepository
from domain.contracts.i_vision_analyzer import IVisionAnalyzer

class VisionService:
    """
    VisionService handles image inspection by decoding base64 images,
    analyzing them for defects using a vision analyzer, and saving the results
    to a fabric repository. It returns the results in a structured DTO format.
    """

    def __init__(self, analyzer: IVisionAnalyzer, repo: IFabricRepository):
        """
        Initializes the VisionService with dependencies.

        :param analyzer: Component responsible for analyzing image data.
        :param repo: Component responsible for persisting defect results.
        """
        self._analyzer = analyzer
        self._repo = repo

    async def inspect_image(self, req: ImageRequestDTO) -> DefectResultDTO:
        """
        Processes an image inspection request.

        - Decodes the base64 image.
        - Analyzes the image for defects.
        - Saves the result to the repository.
        - Returns a DTO with the analysis result.

        :param req: DTO containing base64-encoded image data.
        :return: DTO with defect analysis results.
        """
        # Convert base64 string to raw image bytes
        image_bytes = base64.b64decode(req.image_base64)

        # Analyze the image for defects
        defect_result: DefectResult = await self._analyzer.analyze_image(image_bytes)

        # Persist the result in the repository
        # await self._repo.save_result(defect_result)

        # Return the result as a DTO
        return DefectResultDTO(
            image_id=defect_result.image_id,
            is_defective=defect_result.is_defective,
            probabilities=defect_result.probabilities
        )
