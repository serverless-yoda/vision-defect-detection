# infrastructure/fabric_repository.py

import json
import pyodbc

from domain.contracts.i_fabric_repository import IFabricRepository
from domain.entities.defect_result import DefectResult
from domain.exceptions import FabricRepositoryError
from common.logging import get_logger


logger = get_logger(__name__)

class FabricRepository(IFabricRepository):
    def __init__(self, connection_str: str):
        self.conn_str = connection_str

    async def save_result(self, result: DefectResult) -> None:
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO bronze.defect_results
                    (
                        image_id, timestamp, is_defective, probabilities, raw_response
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    result.image_id,
                    result.timestamp,
                    int(result.is_defective),
                    result.probabilities,
                    json.dumps(result.raw_response)
                )
                conn.commit()
        except Exception as e:
            logger.exception("Fabric ingestion failed")
            raise FabricRepositoryError(str(e))