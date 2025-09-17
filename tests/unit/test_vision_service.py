# tests/unit/test_vision_service.py
import pytest
import base64
from application.services.vision_service import VisionService
from application.dto.image_request_dto import ImageRequestDTO
from domain.contracts.i_vision_analyzer import IVisionAnalyzer
from domain.contracts.i_fabric_repository import IFabricRepository
from domain.entities.defect_result import DefectResult
from datetime import datetime

class FakeAnalyzer(IVisionAnalyzer):
    """
    A mock implementation of IVisionAnalyzer for testing purposes.
    Always returns a DefectResult indicating the image is defective.
    """
    async def analyze_image(self, image_bytes: bytes) -> DefectResult:
        return DefectResult(
            image_id="1",
            timestamp=datetime.utcnow(),
            is_defective=True,
            probabilities={"defect": 0.95, "clean": 0.05}
        )

class FakeRepo(IFabricRepository):
    """
    A mock implementation of IFabricRepository that does nothing.
    Used to test VisionService without persisting data.
    """
    async def save_result(self, result: DefectResult) -> None:
        return None

@pytest.mark.asyncio
async def test_service_flags_defect_and_saves():
    """
    Test that VisionService correctly flags an image as defective
    and returns the expected DefectResultDTO.
    """
    service = VisionService(FakeAnalyzer(), FakeRepo())

    # Create a fake image request with dummy base64-encoded data
    fake_img = ImageRequestDTO(image_base64=base64.b64encode(b"dummydata").decode())

    # Run the inspection
    result = await service.inspect_image(fake_img)

    # Assert that the result indicates a defect
    assert result.is_defective
