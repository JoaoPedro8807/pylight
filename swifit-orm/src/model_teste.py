from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField, IDField

class Pessoa(Model):    
        id = IDField(auto_increment=True)
        nome = CharField(length=50)
        numero = IntegerField(not_null=True)
        data = DateField(not_null=True, default="2021-10-10")   
        ativo = BooleanField(not_null=True, default=True)       