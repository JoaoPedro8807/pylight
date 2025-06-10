from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .field_class import FieldType

if TYPE_CHECKING:
    from backend import DatabaseBackend 
class FieldAbstract(ABC):
    _TYPE: FieldType

    @abstractmethod
    def get_sql_type(self, backend: "DatabaseBackend") -> str:
        pass

    @abstractmethod
    def validate_value(self, value: str) -> bool:
        pass

    @abstractmethod
    def get_create_params(self, **kwargs) -> str:
        pass


        