from ..database_backend import DatabaseBackend
from compilers import SQLCompiler
from main.model.fields.boolean.boolean_field import BooleanField
from typing import TYPE_CHECKING, Dict, Any
from main.model.fields import FieldType

if TYPE_CHECKING:
    from main.model.base.model_base import Model


class PostgreSQLBackend(DatabaseBackend):

    __name__: str = "PostgreSQLBackend"

    SQL_TYPE_MAPPING: Dict[FieldType, Any] = {
            "CharField": lambda length: f"VARCHAR({length})",
            "IntegerField": "INTEGER",
            "IDField": "BIGSERIAL",
            "BooleanField": "BOOLEAN",
            "FloatField": "REAL",
            "DateField": "DATE",
            "TimeField": "TIME",
            #adicionar outros tipos especificos de postgreSQL (fazer check na modelo para ver se o backend suporta)
    }

    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self._compiler = SQLCompiler()

    def connect(self, **kwargs):
        print("executando connect no postgres")
        import psycopg2
        self.__connection = psycopg2.connect(**kwargs)
        self.__cursor = self.__connection.cursor()

    def execute_query(self, query: str, params=None, ):
        try:
            print("executando query", query, params)
            self.__cursor.execute(query, params or ())
        except Exception as e:
            print("Erro ao executar query", e)

    def select_all(self):
        return self.__cursor.fetchall()

    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()

    def add(self, model: "Model", **kwargs) -> None:
        sql, params = self._compiler.insert_sql(backend=self, model=model, **kwargs)
        self.execute_query(sql, params)

    def get_default_conection_params() -> dict:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "user": "postgres",
            "password": "postgres",
        }
    
    def commit(self):
        if self.__connection:
            self.__connection.commit()

    def create_table(self, model: "Model"):
        sql = self._compiler.create_table_sql(backend=self, model=model)
        self.execute_query(sql)
        self.commit()
        
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
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")

    def __name__(self):
        return "PostgreSQLBackend"


    def __exit__(self):
        self.close()