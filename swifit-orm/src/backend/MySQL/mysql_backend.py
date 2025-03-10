from ..database_backend import DatabaseBackend
from typing import Dict, Any

class MySQLBackend(DatabaseBackend):
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

    def __exit__(self):
        self.close()        