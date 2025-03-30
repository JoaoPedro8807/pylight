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
        super().__init__(type=self._TYPE, length=None,  primary_key=True, not_null=None, unique=None, default=None, **kwargs)


    def __set_name__(self, owner: 'Model', name: str):
        self._name = name
        self._model = owner

    def validate_value(self, value: str) -> bool:
        if isinstance(value, int):
            return True
        raise ValueError(f"Invalid value for field '{self._name}'. Expected an integer.")

    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_sql_type("IDField", kwargs=kwargs)

    def get_create_params(self, **kwargs) -> str:
        string_params = ""
        if self._PK:
            string_params += " PRIMARY KEY"
        if self._NOT_NULL:
            string_params += " NOT NULL"
        if self._UNIQUE:
            string_params += " UNIQUE"
        if self._DEFAULT:
            string_params += f" DEFAULT {self._DEFAULT}"
            
        return string_params
    # def __repr__(self):
    #     return f"<IntegerField(name={self._name}, model={self._model.__name__})>"