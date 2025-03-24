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

    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_sql_type("BooleanField", **kwargs)

    def get_create_params(self, **kwargs) -> str:
        string_params = ""
        if self._PK:
            string_params += " PRIMARY KEY"
        if self._NOT_NULL:
            string_params += " NOT NULL"
        if self._UNIQUE:
            string_params += " UNIQUE"
        if self._DEFAULT:
            string_params += f" DEFAULT {int(bool(self._DEFAULT))}"
            
        return string_params