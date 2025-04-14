from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from main.model.fields import FieldType

if TYPE_CHECKING:
    from main.model.base.model_base import Model
class DatabaseBackend(ABC):

    
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def execute_query(self, query: str, params=None):
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def select_all(self):
        pass
    
    @abstractmethod
    def add(self, model: "Model", **kwargs) -> None:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_default_conection_params() -> dict:
        pass    
    @abstractmethod
    def get_sql_type(self, field_type: FieldType, **kwargs) -> str:
        pass
    @abstractmethod    
    def get_supported_date_format(self) -> str:
        pass
    
    @abstractmethod
    def get_create_params_for_bool_field(self, field) -> str:
        pass

    @abstractmethod
    def get_create_params_for_date_field(self, field) -> str:
        pass

    @abstractmethod
    def get_create_params_for_float_field(self, field) -> str: 
        pass

    @abstractmethod
    def get_create_params_for_integer_field(self, field) -> str:
        pass

    @abstractmethod
    def get_create_params_for_char_field(self, field) -> str:
        pass

    @abstractmethod
    def get_create_params_for_id_field(self, field) -> str:
        pass

    # @abstractmethod
    # def name(self) -> str:
    #     pass

    def __exit__(self):
        self.close()
