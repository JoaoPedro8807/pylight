from ..database_backend import DatabaseBackend
from typing import Dict, Any, TYPE_CHECKING, Type, TypeVar
from main.model.fields import FieldType
from compilers import SQLCompiler

if TYPE_CHECKING:
    from main.model.base.model_base import Model

T = TypeVar("T", bound="Model")

class MySQLBackend(DatabaseBackend):

    _compiler = None




    SQL_TYPE_MAPPING: Dict[FieldType, Any] = {
        "CharField": lambda length: f"VARCHAR({length})",
        "IntegerField": "INT",
        "IDField": "INT",
        "BooleanField": "TINYINT(1)",
        "FloatField": "FLOAT",
        "DateField": "DATE",
    }



    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self._compiler = SQLCompiler()
        

    def connect(self, **kwargs):
        import mysql.connector  
        self.__connection = mysql.connector.connect(**kwargs)
        self.__cursor = self.__connection.cursor()

    def execute_query(self, query: str, params=None):
        print("executando query:", query, params)	
        self.__cursor.execute(query, params or ())
    
    def select_all(self, model: "Model"):
        sql, _ = self._compiler.select_all_sql(backend=self, model=model)
        self.execute_query(sql, None)
        return self.fetch_all(sql, None)
        #return self.fetch_all(sql, params)

    def fetch_all(self, sql: str, params=None):
        return self.__cursor.fetchall()
    
    def create_table(self, model: "Model"):
        sql = self._compiler.create_table_sql(backend=self, model=model)
        self.execute_query(sql)
        self.commit()

    def add(self, model, **kwargs):
        print("executando add no mysql")	
        sql, params = self._compiler.insert_sql(backend=self, model=model, **kwargs)
        self.execute_query(sql, params)
    
    def commit(self):
        if self.__connection:
            self.__connection.commit()


    def deseriallize(self, rows: list[tuple], model: Type[T]) -> list[T]:
        """
        Deserializa os dados retornados do banco de dados para instâncias do modelo.
        :param rows: Lista de tuplas com os dados retornados do banco de dados.
        :param model: Classe do modelo correspondente aos dados.
        :return: Lista de instâncias do modelo.
        """
        #column_names = [desc[0] for desc in cursor.description]
        instances: list[T] = []
        for row in rows:
            instance = model.create(**dict(zip(model._fields.keys(), row)))
            instances.append(instance)
        return instances




    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()


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
    

    def get_create_params(self, field, default_formatter=None) -> str:
        """
        Gera os parâmetros de criação de um campo genérico.
        :param field: O campo para o qual os parâmetros serão gerados.
        :param default_formatter: Função opcional para formatar o valor padrão.
        :return: String com os parâmetros de criação.
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

        if field._AUTO_INCREMENT:
            string_params += " AUTO_INCREMENT"

        return string_params

    def get_create_params_for_bool_field(self, field) -> str:
        # MySQL usa TINYINT(1) para booleanos, e valores padrão são 0 ou 1
        return self.get_create_params(field, default_formatter=lambda val: 1 if val else 0)

    def get_create_params_for_char_field(self, field) -> str:
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")

    def get_create_params_for_integer_field(self, field) -> str:
        return self.get_create_params(field)

    def get_create_params_for_date_field(self, field) -> str:
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")

    def get_create_params_for_float_field(self, field) -> str:
        return self.get_create_params(field)
    
    def get_create_params_for_id_field(self, field):
        return self.get_create_params(field, default_formatter=lambda val: f"'{val}'")


    @property
    def cursor(self):
        return self.__cursor


    def __name__(self) -> str:
        return "MySQLBackend"

    def __enter__(self):
        return self
    

    def __exit__(self):
        self.close()        