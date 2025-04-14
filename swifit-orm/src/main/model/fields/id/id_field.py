from typing import TYPE_CHECKING
from ..field_abstract import FieldAbstract
from ..field_class import Field

if TYPE_CHECKING:
    from backend import DatabaseBackend
    from main.model import Model

class IDField(FieldAbstract, Field):

    """
    Campo de número inteiro.
    """
    _TYPE = "IDField" 
    _name: str
    _model: 'Model'

    def __init__(self, auto_increment: bool = True, **kwargs):
        super().__init__(type=self._TYPE, auto_increment=auto_increment, length=None,  primary_key=True, not_null=None, unique=None, default=None, **kwargs)


    def __set_name__(self, owner: 'Model', name: str):
        self._name = name
        self._model = owner

    def validate_value(self, value: str, **kwargs) -> bool:
        if not self._AUTO_INCREMENT:
            if isinstance(value, int):
                return True
            raise ValueError(f"Valor inválido para o campo '{self._name}'.")
        return True

    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_sql_type("IDField", kwargs=kwargs)

    def get_create_params(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_create_params_for_id_field(field=self, **kwargs)

        
            
    # def __repr__(self):
    #     return f"<IntegerField(name={self._name}, model={self._model.__name__})>"