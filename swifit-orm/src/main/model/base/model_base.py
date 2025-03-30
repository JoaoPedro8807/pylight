from ..fields import Field, FieldAbstract
from typing import Dict
from ...session import Session
from backend import DatabaseBackend
from ...exceptions import  ModelValueError

class ModelBase(type):
    """
    Metaclasse usada para criar classes de modelos.
    """
    def __new__(cls, name, bases, attrs):
        if name == 'Model' and bases == ():
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        print("attrs: ", attrs)                
        print("Campos: ", fields)
        print("classes: ", bases)
        print("name: ", name)
        

        attrs['_fields'] = fields

        meta = attrs.get('Meta', None)
        db_table = getattr(meta, 'db_table', None)
        if not db_table:
            db_table = str(name).lower().strip()
        attrs['_meta'] = {'db_table': db_table}


        attrs['save'] = cls.save
        attrs['delete'] = cls.delete
        attrs['objects'] = cls.objects

        # 6. Cria a classe final
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def save(self):
        """
        Método save() padrão.
        """
        print(f"Salvando {self.__class__.__name__} na tabela {self._meta['db_table']}")

    @staticmethod
    def delete(self):
        """
        Método delete() padrão.
        """
        print(f"Deletando {self.__class__.__name__} da tabela {self._meta['db_table']}")

    @staticmethod
    def objects(self):
        """
        Manager padrão.
        """
        print(f"Acessando objetos de {self.__class__.__name__} na tabela {self._meta['db_table']}")


class ModelState:
    db: str
    adding : bool




class Model(metaclass=ModelBase):
    """
    Classe base para modelos.
    """
    _fields: Dict[str, FieldAbstract]
    _state = ModelState
    _session: Session = None
    _instance: 'Model' = None
    _name: str = None



    def __init__(self, **kwargs):
        self._session = kwargs.get('session', None)
        print("fields: ", self._fields)

    def __set_name__(self, owner, name):
        self._instance = owner
        self._name = name

    def validate_data(fields: Dict[str, FieldAbstract], params: Dict[str, str]) -> None:
        """Valida os dados fornecidos para o modelo."""
        for field_name, field in fields.items():
            if field._NOT_NULL and field_name not in params:
                raise ModelValueError(f"Campo '{field_name}' não encontrado nos parâmetros.")
            
            value = params[field_name]
            if not field.validate_value(value):
                raise ModelValueError(f"Valor inválido para o campo '{field_name}': {value}")

    @classmethod    
    def validate_field(cls, field_name: str) -> None:
        if field_name not in cls._fields.keys():
            raise ModelValueError(f"Campo '{field_name}' não é válido para o modelo '{cls.__name__}'.")
        
    @classmethod
    def validate_all(cls, **kwargs) -> None:
        for field_name, value in kwargs.items():
            cls.validate_field(field_name)
        cls.validate_data(fields=cls._fields, params=kwargs)


    @classmethod
    def create(cls, session: Session, **kwargs) -> 'Model':
        """
        Cria um novo objeto no banco de dados com base nos campos definidos no modelo.
        """

        backend = session.engine.backend
        backend.add(cls, **kwargs)

        cls.validate_all(**kwargs)

        # Retorna uma instância do modelo
        instance = cls(session=session, **kwargs)
        for field_name, value in kwargs.items():
            setattr(instance, field_name, value)
        return instance
    
    def save(self):
        if not self._session:
            raise ValueError("O objeto precisa estar vinculado a uma sessão para ser salvo.")
        
        self._session.commit()
        print(f"Salvando {self} na tabela {self._meta['db_table']}")


    def __exit__(self, type, value, traceback):
        if self._state.adding:
            self._session.commit()
            self._state.adding = False
        self._session = None
        

    @property
    def fields(self) -> Dict[str, FieldAbstract]:
        return self._fields

    def __str__(self):
        return f"{self.__class__.__name__}"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}>"