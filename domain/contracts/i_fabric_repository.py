# domain/contracts/i_fabric_repository.py

# Importing Abstract Base Class (ABC) and abstractmethod to define an interface-like class
from abc import ABC, abstractmethod

# Importing DefectResult, which likely represents the outcome of a vision analysis or defect detection process
from domain.entities.defect_result import DefectResult


class IFabricRepository(ABC):
    """
    IFabricRepository is an abstract base class (interface) that defines the contract
    for any repository responsible for persisting defect analysis results into a storage system.
    
    Implementations of this interface will handle saving DefectResult objects to a database,
    data lake, or any other persistence layer.
    """

    @abstractmethod
    async def save_result(self, result: DefectResult) -> None:
        """
        Save the given defect analysis result to the underlying storage system.

        Args:
            result (DefectResult): The result object containing details of the defect analysis
                                   (e.g., defect type, severity, metadata).

        Returns:
            None: This method does not return any value.

        Note:
            This method is asynchronous and must be awaited when called.
        """
        pass
