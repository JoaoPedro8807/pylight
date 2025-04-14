from ..field_class import Field
from ..field_abstract import FieldAbstract
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from main.model.fields.field_class import FieldType

if TYPE_CHECKING:
    from main.model import Model
    from backend import DatabaseBackend
    

class CharField(FieldAbstract, Field):
    _TYPE = "CharField"
    _name: str = ""
    _model: 'Model' = None
    """
    Campo de texto.
    """
    def __init__(self, 
            length: int = 255, 
            primary_key: bool = False, 
            not_null: bool = False, 
            unique: bool = False, 
            default: str = None, 
            **kwargs):          
        super().__init__(type=self._TYPE, length=length, primary_key=primary_key, not_null=not_null, unique=unique, default=default, **kwargs)  

    def __set_name__(self, owner: 'Model', name: str):
        self._name = name
        self._model = owner


    def get_sql_type(self, backend: "DatabaseBackend", **kwargs) -> str:
        return backend.get_sql_type("CharField", length=self._LENGTH)
    
    def validate_value(self, value, **kwargs) -> bool:
        if len(value) > self._LENGTH:
            raise ValueError(f"O campo {self._name} excede o tamanho permitido de {self._LENGTH} caracteres.")
        return True
    
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

    # def __repr__(self, **kwargs):
    #     return f"<CharField(name={self._name}, model={self._model.__name__})>"

        