from ..fields import Field, FieldAbstract
from typing import Dict
from ...session import Session
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


        attrs['meta_save'] = cls.save
        attrs['meta_delete'] = cls.delete
        attrs['meta_objects'] = cls.objects

        # 6. Cria a classe final
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def save(self, **kwargs):
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
    _original_state: dict = None
    id: str = None




    def __init__(self, **kwargs):
        self._session = kwargs.get('session', None)
        self._original_state = self.get_field_values()

    def __set_name__(self, owner, name):
        self._instance = owner
        self._name = name
    def get_changes(self) -> dict:
        """
        Retorna os campos que foram alterados desde o último rastreamento.

        Returns:
            dict: Um dicionário com os campos alterados e seus novos valores.
        """
        current_state = self.get_field_values()
        return {
            field: value
            for field, value in current_state.items()
            if self._original_state.get(field) != value
        }
    
    def update_original_state(self):
        """
        Atualiza o estado original para refletir o estado atual.
        """
        self._original_state = self.get_field_values()

    def to_json(self): #APENAS TESTE
        return {
            "id": self.id,
            "nome": self.nome,
            "numero": self.numero,
            "data": str(self.data),
            "ativo": self.ativo
        }

    def validate_data(self, **kwargs) -> None:
        """Valida os dados fornecidos para o modelo."""
        fields = self._fields
        params = {}

        for field_name, field in fields.items():
            for attr, value in self.__dict__.items():
                if attr == field_name:
                    params[field_name] = value
            self.validate_field(field_name)
            if field._NOT_NULL and field_name not in params:
                raise ModelValueError(f"O campo '{field_name}' é obrigatório.")
            
            if field._AUTO_INCREMENT and field_name not in params:
                params[field_name] = None
            try:
                value = params[field_name]
                if not field.validate_value(value, **kwargs):
                    raise ModelValueError(f"Valor inválido para o campo '{field_name}': {value}")
            except KeyError:
                raise ModelValueError(f"O campo '{field_name}' é obrigatório.")
            
    @classmethod    
    def validate_field(cls, field_name: str) -> None:
        if field_name not in cls._fields.keys():
            raise ModelValueError(f"Campo '{field_name}' não é válido para o modelo '{cls.__name__}'.")
        
    
    def validate_all(self, **kwargs) -> None:
        self.validate_data(**kwargs)


    @classmethod
    def create(cls, **kwargs) -> 'Model':
        """
        Cria um novo objeto no banco de dados com base nos campos definidos no modelo.
        """
        #cls.validate_all(**kwargs)

        # Retorna uma instância do modelo
        instance = cls(**kwargs)

        for field_name, value in kwargs.items():    
            setattr(instance, field_name, value)

        # Atualiza o estado original para refletir os valores iniciais
        instance._original_state = instance.get_field_values()
        
        return instance
    
    # def add(self, session: Session = None, commit: bool = True, **kwargs) -> None:
    #     self._session = session or self._session

    #     if not self._session:
    #         raise ModelValueError("O objeto precisa estar vinculado a uma sessão para ser salvo.")
        
    #     backend = session.engine.backend
    #     self.validate_all(backend=backend)
    #     backend.add(self, **kwargs)
        
    #     if commit:
    #         self._session.commit()
            
    #     print(f"Salvando {self} na tabela {self._meta['db_table']}")

    # def save(self):
    #     if not self._session:
    #         raise ModelValueError("O objeto precisa estar vinculado a uma sessão para ser salvo.")
        
    #     return self._session.engine.backend.commit
        
    def get_field_values(self) -> dict:
        """
        Retorna um dicionário contendo os atributos do modelo que são instâncias de Field.

        Returns:
            dict: Um dicionário com os nomes dos campos como chaves e os valores como valores.
        """
        return {
            field_name: getattr(self, field_name)
            for field_name, field in self._fields.items()
            if isinstance(field, Field) and not field._AUTO_INCREMENT
        }


    def __exit__(self, type, value, traceback):
        if self._state.adding:
            self._session.commit()
            self._state.adding = False
        self._session = None
        
    @property
    def id(self) -> str:
        return self.id
    
    @id.setter
    def id(self, value: str) -> None:
        self.id = value

    @property
    def fields(self) -> Dict[str, FieldAbstract]:
        return self._fields


    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f"{self.__class__.__name__}"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}>"