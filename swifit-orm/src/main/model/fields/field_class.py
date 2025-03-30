from typing import Literal
from typing import TYPE_CHECKING


FieldType = Literal[
    "CharField", 
    "IntegerField", 
    "DateField", 
    "BooleanField", 
    "FloatField",
    "TimeField",
    "IDField",

    ]   


class Field:
    """
    Classe base para campos de modelo.
    """
    _TYPE: FieldType
    _LENGTH: int
    _PK: bool
    _NOT_NULL: bool
    _UNIQUE: bool
    _DEFAULT: str
    _OPTIONS: dict
    _AUTO_INCREMENT: bool


    def __init__(self, type: FieldType, length: int = 255, primary_key: bool = False, not_null: bool = False, unique: bool = False, default: str = None, auto_increment: bool = False, **kwargs):
        self._TYPE = type
        self._LENGTH = length
        self._PK = primary_key
        self._NOT_NULL = not_null
        self._UNIQUE = unique
        self._DEFAULT = default or None
        self._OPTIONS = kwargs
    




    def __str__(self):
        return f"{self.__class__.__name__}"
