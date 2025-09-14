# domain/exceptions.py

class VisionAnalysisError(Exception):
    """Thrown when Azure Vision analysis failed"""

class FabricRepositoryError(Exception):
    """Thrown when Microsoft Fabric pipeline ingestion failed"""