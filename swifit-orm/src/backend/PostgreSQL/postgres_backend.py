from ..database_backend import DatabaseBackend
from compilers import SQLCompiler
from typing import TYPE_CHECKING, Dict, Any, List, Optional, TypeVar, Type
from main.filters import BaseFilter
from main.model.fields import FieldType
from main.exceptions import SqlCompilerException

if TYPE_CHECKING:
    from main.model.base.model_base import Model

T = TypeVar("T", bound="Model")

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
            raise SqlCompilerException(f"Erro ao executar a query: {query} com os parâmetros: {params}") from e
    
    def fetch_all(self, sql: str, params=None):
        return self.__cursor.fetchall()
    
    def deseriallize(self, rows: list[tuple], model: Type[T]) -> list[T]:
        instances: list[T] = []
        for row in rows:
            instance = model.create(**dict(zip(model._fields.keys(), row)))
            instances.append(instance)
        return instances

    def get_id(self):
        res = self.__cursor.fetchone()
        if not res:
            raise SqlCompilerException("Erro ao obter o ID do registro inserido.")
        return res[0]


    def add(self, model: "Model", **kwargs) -> None:
        sql, params = self._compiler.insert_sql(backend=self, model=model, returning_id=True,  **kwargs)
        self.execute_query(sql, params)
        id = self.get_id()
        print("id para ser inserido no model: ", id)
        model.id = id

    def select(self, model: "Model", filters: Optional[List[BaseFilter]],  **kwargs):
        sql, params = self._compiler.select_sql(backend=self, filters=filters,  model=model, **kwargs)
        self.execute_query(sql, params)
        rows = self.fetch_all(sql, params)
        if not rows:
            print("Nenhum registro encontrado")
            return None
        return self.deseriallize(rows, model)
        
    def update(self, model: "Model", **kwargs) -> None:
        sql, params = self._compiler.update_sql(backend=self, model=model, **kwargs)
        self.execute_query(sql, params)
        self.commit()

    def delete(self, model: "Model", **kwargs) -> None:
        sql, params = self._compiler.delete_sql(backend=self, model=model, **kwargs)
        self.execute_query(sql, params)
        self.commit()

    def select_all(self, model: "Model"):
        sql, _ = self._compiler.select_all_sql(backend=self, model=model)
        self.execute_query(sql, None)
        rows = self.fetch_all(sql, None)
        return self.deseriallize(rows, model)
    
    def create_table(self, model: "Model"):
        sql = self._compiler.create_table_sql(backend=self, model=model)
        self.execute_query(sql)
        self.commit()
        
    def get_sql_type(self, field_type: FieldType, length: int = 255, **kwargs) -> str:
        sql_type = self.SQL_TYPE_MAPPING[field_type]
        if callable(sql_type):
            return sql_type(length)
        return sql_type or "TEXT"



    def get_default_conection_params() -> dict:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "user": "postgres",
            "password": "postgres",
        }


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

    def commit(self):
        if self.__connection:
            self.__connection.commit()

    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()


    @property
    def cursor(self):
        return self.__cursor


    def __name__(self):
        return "PostgreSQLBackend"


    def __exit__(self):
        self.close() 