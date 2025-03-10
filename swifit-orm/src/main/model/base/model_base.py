from fields import Field
from typing import Dict

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
    _fields: Dict[str, Field]
    _state = ModelState

    def __init__(self, **kwargs):
        print("fields: ", self._fields)

    
    @property
    def fields(self) -> Dict[str, Field]:
        return self._fields

    pass

