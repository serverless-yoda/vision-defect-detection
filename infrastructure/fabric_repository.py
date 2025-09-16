# infrastructure/fabric_repository.py

import json
import pyodbc

from domain.contracts.i_fabric_repository import IFabricRepository
from domain.entities.defect_result import DefectResult
from domain.exceptions import FabricRepositoryError
from common.logging import get_logger

logger = get_logger(__name__)

class FabricRepository(IFabricRepository):
    """
    FabricRepository handles the persistence of defect analysis results
    into a Microsoft Fabric-connected SQL database using pyodbc.

    Attributes:
        conn_str (str): The connection string used to connect to the database.
    """

    def __init__(self, connection_str: str):
        """
        Initializes the repository with the given database connection string.

        Args:
            connection_str (str): ODBC connection string for the target database.
        """
        self.conn_str = connection_str

    async def save_result(self, result: DefectResult) -> None:
        """
        Saves a DefectResult object into the bronze.defect_results table.

        Args:
            result (DefectResult): The result object containing image analysis data.

        Raises:
            FabricRepositoryError: If the database operation fails.
        """
        try:
            # Establish a connection to the database
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()

                # Execute the insert statement with parameters
                cursor.execute(
                    """
                    INSERT INTO bronze.defect_results (
                        image_id, timestamp, is_defective, probabilities, raw_response
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    result.image_id,
                    result.timestamp,
                    int(result.is_defective),  # Convert boolean to int (0 or 1)
                    result.probabilities,
                    json.dumps(result.raw_response)  # Serialize raw response to JSON
                )

                # Commit the transaction
                conn.commit()

        except Exception as e:
            # Log and raise a custom error if the operation fails
            logger.exception("Fabric ingestion failed")
            raise FabricRepositoryError(str(e))
