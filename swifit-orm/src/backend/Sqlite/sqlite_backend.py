from ..database_backend import DatabaseBackend
from typing import TypedDict
from compilers import SQLCompiler
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING 
from main.model.fields import FieldType

if TYPE_CHECKING:
    from main.model.fields import FieldType

class SqliteBackend(DatabaseBackend):

    __db_file: str | Path
    

    SQL_TYPE_MAPPING: Dict[FieldType, str] = {
    "CharField": "TEXT",
    "IntegerField": "INTEGER",
    "BooleanField": "INTEGER",  # SQLite não tem tipo booleano nativo
    "DateField": "TEXT",
}

    def __init__(self, db_file: str | Path = None, **kwargs):
        self.connection = None
        self.cursor = None
        self._compiler = SQLCompiler()
        self.__db_file = db_file

    def connect(self, **kwargs):
        import sqlite3
        print("executando connect no sqlite", "dbfile: ", self.__db_file)   
        self.connection = sqlite3.connect(self.__db_file)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params=None):
        try:
            self.cursor.execute(query, params or ())
        except Exception as e:
            print("Erro ao executar query", e)

    def fetch_all(self):
        return self.cursor.fetchall()
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_default_conection_params() -> dict:
        return {
            "database": ":memory:"
        }
    
    def create_table(self, model):
        print("criando tabela", model)
        sql = self._compiler.create_table_sql(backend=self, model=model)
        self.execute_query(sql)

    def get_sql_type(self, field_type: FieldType, **kwargs) -> str:
        return self.SQL_TYPE_MAPPING[field_type]

    def get_supported_date_format(self) -> str:
        """
        Retorna o formato de data suportado pelo SQLite.
        """
        return "%Y-%m-%d"  # Formato ISO 8601

    @property
    def db_file(self) -> str | Path:
        return self.__db_file
    
    @db_file.setter
    def db_file(self, db_file: str | Path) -> None:
        self.__db_file = db_file

    def __enter__(self):
        return self
    
    def __name__(self):
        return self.__class__.__name__


    def __exit__(self):
        self.close()

    