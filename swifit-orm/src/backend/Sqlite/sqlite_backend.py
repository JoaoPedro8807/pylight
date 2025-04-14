from ..database_backend import DatabaseBackend
from typing import TypedDict
from compilers import SQLCompiler
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING 
from main.model.fields import FieldType

if TYPE_CHECKING:
    from main.model.fields import FieldType
    from main.model.base.model_base import Model


class SqliteBackend(DatabaseBackend):
    __db_file: str | Path
    

    SQL_TYPE_MAPPING: Dict[FieldType, str] = {
    "CharField": "TEXT",
    "IDField": "INTEGER",
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
        print("executando query:", query, params)
        try:
            self.cursor.execute(query, params or ())
        except Exception as e:
            print("Erro ao executar query", e)

    def select_all(self):
        return self.cursor.fetchall()
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


    def add(self, model, **kwargs):
        sql, params = self._compiler.insert_sql(backend=self, model=model, **kwargs)
        self.execute_query(sql, params)

    def commit(self) -> None:
        if self.connection:
            self.connection.commit()

    def get_default_conection_params() -> dict:
        return {
            "database": ":memory:"
        }
    
    def create_table(self, model: "Model"):
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
    
    def get_create_params(self, field, default_formatter: callable = None) -> str:
        """
        Gera os parâmetros de criação de um campo genérico.
        * param field: O campo para o qual os parâmetros serão gerados.
        * param default_formatter: Função opcional para formatar o valor padrão.
        """
        string_params = ""
        if field._PK:
            string_params += " PRIMARY KEY"
        if field._NOT_NULL:
            string_params += " NOT NULL"
        if field._UNIQUE:
            string_params += " UNIQUE"
        if field._DEFAULT is not None:
            if default_formatter:
                string_params += f" DEFAULT {default_formatter(field._DEFAULT)}"
            else:
                string_params += f" DEFAULT {field._DEFAULT}"
        return string_params

    def get_create_params_for_bool_field(self, field) -> str:
        return self.get_create_params(field, default_formatter=lambda val: 'TRUE' if val else 'FALSE')

    def get_create_params_for_char_field(self, field) -> str:
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")  # Strings precisam de aspas simples

    def get_create_params_for_integer_field(self, field) -> str:
        return self.get_create_params(field)  # Inteiros não precisam de formatação especial

    def get_create_params_for_date_field(self, field) -> str:
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")  # Datas precisam de aspas simples

    def get_create_params_for_float_field(self, field) -> str:
        return self.get_create_params(field)  # Floats não precisam de formatação especial


    def get_create_params_for_id_field(self, field):
        return self.get_create_params(field)  # IDField é tratado como INTEGER no SQLite
 

    @property
    def db_file(self) -> str | Path:
        return self.__db_file
    
    @property
    def name(self) -> str:
        return self.__name__
    
    @db_file.setter
    def db_file(self, db_file: str | Path) -> None:
        self.__db_file = db_file

    def __enter__(self):
        return self
    
    def __name__(self):
        return "SqliteBackend"


    def __exit__(self):
        self.close()

    