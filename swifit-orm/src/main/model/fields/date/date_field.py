from datetime import datetime
from ..field_class import Field
from typing import TYPE_CHECKING, Union
from datetime import date, datetime

from main.exceptions import ModelValueError

if TYPE_CHECKING:
    from main.model import Model
    from backend import DatabaseBackend

class DateField(Field):
    _TYPE = "DateField"
    _name: str
    _model: 'Model'

    def __init__(self, primary_key=False, not_null=False, default=None):
        if default:
            default = f"'{default}'" #escape string para sqlite para date padrão no valor padrão
        super().__init__(type=self._TYPE, primary_key=primary_key, not_null=not_null, default=default)
     

    def __set_name__(self, owner, name):
        self._model = owner
        self._name = name

    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        """
        Retorna o tipo SQL correspondente com base no backend.
        """
        return backend.get_sql_type("DateField", **kwargs)

        

    def validate_value(self, value: Union[str, datetime, datetime.date], **kwargs) -> bool:
        """
        Valida o valor fornecido para o campo de data.
    
        Args:
            value (str): O valor da data a ser validado.
            backend (DatabaseBackend): O backend que define o formato de data suportado.
    
        Returns:
            bool: True se o valor for válido, caso contrário, levanta uma exceção.
    
        Raises:
            ValueError: Se o valor não estiver no formato esperado.
        """
        if not isinstance(value, (str, datetime, date)): 
            raise ValueError(
                f"Valor da data inválido '{self._name}'. recebido {value, type(value)} "
            )
    
        backend: DatabaseBackend = kwargs.get("backend")
        # Valida o formato da data com base no backend
        supported_format = backend.get_supported_date_format()

        if isinstance(value, (datetime, date)):
            value = value.strftime(supported_format)

        try:
            datetime.strptime(value, supported_format)
            return True
        
        except ValueError:
            raise ModelValueError(
                f"Valor da data inválido '{self._name}'. "
                f"Formato esperado: {supported_format}, formato recebido: {value}"
            )
        

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