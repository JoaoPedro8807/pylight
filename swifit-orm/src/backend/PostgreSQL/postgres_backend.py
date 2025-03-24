from ..database_backend import DatabaseBackend
from compilers import SQLCompiler
from main.model.base.model_base import Model
from typing import TYPE_CHECKING, Dict, Any
from main.model.fields import FieldType

class PostgreSQLBackend(DatabaseBackend):

    SQL_TYPE_MAPPING: Dict[FieldType, Any] = {
            "CharField": lambda length: f"VARCHAR({length})",
            "IntegerField": "INTEGER",
            "BooleanField": "BOOLEAN",
            "FloatField": "REAL",
            "DateField": "DATE",
    }


    def __init__(self):
        self.connection = None
        self.cursor = None
        self._compiler = SQLCompiler

    def connect(self, **kwargs):
        print("executando connect no postgres")
        import psycopg2
        self.connection = psycopg2.connect(**kwargs)
        self.cursor = self.connection.cursor()

    def execute_query(self, query: str, params=None):
        self.cursor.execute(query, params or ())

    def fetch_all(self):
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_default_conection_params() -> dict:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "user": "postgres",
            "password": "postgres",
        }
    
    def create_table(self, model: Model):
        sql = self._compiler.create_table_sql(model)
        self.execute_query(sql)
        
    def get_sql_type(self, field_type: FieldType, length: int = 255, **kwargs) -> str:
        sql_type = self.SQL_TYPE_MAPPING[field_type]
        if callable(sql_type):
            return sql_type(length)
        return sql_type or "TEXT"

    def get_supported_date_format(self) -> str:
        """
        Retorna o formato de data suportado pelo PostgreSQL.
        """
        return "%Y-%m-%d"  # Formato ISO 8601

    def __exit__(self):
        self.close()