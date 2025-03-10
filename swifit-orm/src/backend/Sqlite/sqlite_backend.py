from ..database_backend import DatabaseBackend
from typing import TypedDict
from compilers import SQLCompiler
from os import Path
class SqliteBackend(DatabaseBackend):

    __db_file: str | Path

    def __init__(self, db_file: str | Path = None, **kwargs):
        self.connection = None
        self.cursor = None
        self._compiler = SQLCompiler
        self.__db_file = db_file

    def connect(self, **kwargs):
        import sqlite3
        self.connection = sqlite3.connect(self.__db_file, **kwargs)
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
    
    def create_table(self, model):
        print("criando tabela")
        sql = self._compiler.create_table_sql(model)
        self.execute_query(sql)

    @property
    def db_file(self) -> str | Path:
        return self.__db_file
    
    @db_file.setter
    def db_file(self, db_file: str | Path) -> None:
        self.__db_file = db_file

    def __enter__(self):
        return self


    def __exit__(self):
        self.close()

    