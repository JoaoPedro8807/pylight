from fields import Field

class ModelBase(type):
    """
    Metaclasse usada para criar classes de modelos.
    """
    def __new__(cls, name, bases, attrs):
        if name == 'Model' and bases == ():
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        for attr_name, attr_value in attrs.items():
            print("Atributo: ", attr_name, "Valor: ", attr_value)
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        print("Campos: ", fields)
        print("classes: ", bases)
        

        # 3. Adiciona os campos à classe
        attrs['_fields'] = fields

        # 4. Define o nome da tabela no banco de dados
        meta = attrs.get('Meta', None)
        db_table = getattr(meta, 'db_table', None)
        if not db_table:
            # Se não houver nome personalizado, usa a convenção
            db_table = f"{name.lower()}"
        attrs['_meta'] = {'db_table': db_table}

        # 5. Adiciona métodos padrão à classe
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



class Model(metaclass=ModelBase):
    """
    Classe base para modelos.
    """
    pass