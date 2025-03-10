from base import ModelBase, Model
from typing import Dict 
from fields import Field, CharField

class Teste:
    pass


class SwifitModel(Model):
    _fields: Dict[str, Field]
        
    nome = CharField(length=50)
    class Meta:
        db_table = 'swifit_model'
    pass



t = SwifitModel()

