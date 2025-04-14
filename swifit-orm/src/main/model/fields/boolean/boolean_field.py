from ..field_abstract import FieldAbstract
from ..field_class import Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend import DatabaseBackend
    from main.model import Model
    from fields import FieldType

class BooleanField(FieldAbstract, Field):
    _TYPE = "BooleanField"
    _name: str
    _model: 'Model'


    def __init__(self, primary_key=False, not_null=False, default=None):
        super().__init__(type=self._TYPE, primary_key=primary_key, not_null=not_null, default=default)

    def __set_name__(self, owner: 'Model', name: str):
        self._name = name
        self._model = owner

    def validate_value(self, value: str, **kwargs) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"Valor inválido para o campo '{self._name}'. Esperado: True ou False.")
        return True
        # try:
        #     value = bool(value)
        # except ValueError:
        #     raise ValueError(f"Valor inválido para '{self._name}'. Esperado: True ou False.")
        # return value


    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_sql_type("BooleanField", **kwargs)

    def get_create_params(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_create_params_for_bool_field(field=self)       
          