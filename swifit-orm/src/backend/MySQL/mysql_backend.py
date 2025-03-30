from ..database_backend import DatabaseBackend
from typing import Dict, Any, TYPE_CHECKING
from main.model.fields import FieldType




class MySQLBackend(DatabaseBackend):


    SQL_TYPE_MAPPING: Dict[FieldType, Any] = {
        "CharField": lambda length: f"VARCHAR({length})",
        "IntegerField": "INT",
        "IDField": "INT",
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

    def add(self, model, **kwargs):
        pass
    

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



    def __exit__(self):
        self.close()        