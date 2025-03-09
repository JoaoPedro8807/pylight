from ..database_backend import DatabaseBackend
from typing import TypedDict
class SqliteBackend(DatabaseBackend):

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, **kwargs):
        import sqlite3
        self.connection = sqlite3.connect(**kwargs)
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
            "database": ":memory:"
        }
        


    def __exit__(self):
        self.close()