from . import Query
from compilers import SQLCompiler
class UpdateQuery(Query):
    def __init__(self, model):
        super().__init__(model)
        self.values = {}  # Campos e valores a serem atualizados
        self.filters = {}  # Filtros para a cláusula WHERE

    def add_update_fields(self, values):
        """
        Define os campos e valores a serem atualizados.
        """
        self.values.update(values)

    def add_filter(self, field, value):
        """
        Adiciona um filtro para a cláusula WHERE.
        """
        self.filters[field] = value

    def get_compiler(self, using=None, connection=None):
        """
        Retorna o compilador de SQL para gerar a consulta.
        """
        if using is None and connection is None:
            raise ValueError("É necessário fornecer 'using' ou 'connection'.")
        return SQLCompiler()
        #return super().get_compiler(using=using, connection=connection)