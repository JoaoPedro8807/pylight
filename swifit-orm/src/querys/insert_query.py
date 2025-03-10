from .query import Query
from main.model import Model
class InsertQuery(Query):
    def __init__(self, model: Model):
        super().__init__(model)
        self.fields = []  # Campos a serem inseridos
        self.objs = []   # Objetos a serem inseridos

    def insert_values(self, fields, objs, raw=False):
        """
        Define os campos e valores a serem inseridos.
        """
        self.fields = fields
        self.objs = objs
        self.raw = raw

    def get_compiler(self, using=None, connection=None):
        """
        Retorna o compilador de SQL para gerar a consulta.
        """
        if using is None and connection is None:
            raise ValueError("É necessário fornecer 'using' ou 'connection'.")
        return super().get_compiler(using=using, connection=connection)