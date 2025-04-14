from datetime import datetime
from ..field_class import Field
from ..field_abstract import FieldAbstract
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main.model import Model
    from backend import DatabaseBackend

class TimeField(FieldAbstract, Field):
    _TYPE = "TimeField"
    _name: str
    _model: 'Model'

    def __init__(self, primary_key=False, not_null=False, default=None):
        super().__init__(type=self._TYPE, primary_key=primary_key, not_null=not_null, default=default)
     

    def validate_value(self, value: str, **kwargs) -> bool:
        try:
            datetime.strptime(value, "%H:%M:%S")
            return True
        except ValueError:
            raise ValueError(
                f"Valor inválido para o campo '{self._name}'. "
                f"É esperado o formato: HH:MM:SS, obtido: {value}"
            )


    def __set_name__(self, owner, name):
        self._model = owner
        self._name = name

    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        """
        Retorna o tipo SQL correspondente com base no backend.
        """
        return backend.get_sql_type("TimeField", **kwargs)

    def get_create_params(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_create_params_for_date_field(field=self, **kwargs)

    def validate_date_format(self, date_value: str, backend: "DatabaseBackend") -> bool:
        supported_format = backend.get_supported_date_format()
        try:
            datetime.strptime(date_value, supported_format)
            return True
        except ValueError:
            raise ValueError(
                f"Invalid date format for field '{self._name}'. "
                f"Expected format: {supported_format}"
            )

    # def __repr__(self):
    #     return f"<DateField(name={self._name}, model={self._model.__name__})>"