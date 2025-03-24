from ..database_backend import DatabaseBackend
from typing import Dict, Any, TYPE_CHECKING
from main.model.fields import FieldType




class MySQLBackend(DatabaseBackend):


    SQL_TYPE_MAPPING: Dict[FieldType, Any] = {
        "CharField": lambda length: f"VARCHAR({length})",
        "IntegerField": "INT",
        "BooleanField": "TINYINT(1)",
        "FloatField": "FLOAT",
        "DateField": "DATE",
    }



    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, **kwargs):
        import mysql.connector  
        self.connection = mysql.connector.connect(**kwargs)
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


    def get_default_conection_params() -> Dict[str, int | str]:
        return {
            "host": "localhost",
            "port": 3306,
            "database": "mysql",
            "user": "root",
            "password": "root",
        }
    
    def get_sql_type(self, field_type: FieldType, **kwargs) -> str:
        sql_type = self.SQL_TYPE_MAPPING[field_type]
        if callable(sql_type):
            return sql_type(**kwargs)
        return sql_type

    
    def get_supported_date_format(self) -> str:
        """
        Retorna o formato de data suportado pelo MySQL.
        """
        return "%Y-%m-%d"  # Formato ISO 8601

    def __exit__(self):
        self.close()        