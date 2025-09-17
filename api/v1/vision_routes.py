from fastapi import APIRouter, Depends
from application.dto.defect_result_dto import DefectResultDTO
from application.dto.image_request_dto import ImageRequestDTO
from application.services.vision_service import VisionService
from infrastructure.azure_vision_analyzer import AzureVisionAnalyzer
from infrastructure.fabric_repository import FabricRepository
from common.config import settings

# Create a router instance for vision-related API endpoints
router = APIRouter()

def get_service() -> VisionService:
    """
    Dependency provider for VisionService.

    Initializes VisionService with:
    - AzureVisionAnalyzer: for image defect analysis
    - FabricRepository: for saving results, using the configured connection string
    """
    return VisionService(
        AzureVisionAnalyzer(),
        FabricRepository(settings.fabric_connection_string)
    )

@router.post("/inspect", response_model=DefectResultDTO)
async def inspect(req: ImageRequestDTO, service: VisionService = Depends(get_service)):
    """
    Endpoint to inspect an image for defects.

    - Accepts a POST request with base64-encoded image data.
    - Uses VisionService to analyze the image and determine defect status.
    - Returns the result as a DefectResultDTO.

    :param req: ImageRequestDTO containing the base64 image.
    :param service: VisionService instance provided via dependency injection.
    :return: DefectResultDTO with analysis results.
    """
    return await service.inspect_image(req)
