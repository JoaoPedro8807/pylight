from backends.database_backend import DatabaseBackend
from typing import Literal, TypedDict
from backends import SqliteBackend, MySQLBackend, PostgreSQLBackend 
from exceptions import SwifitORMException

class SwifitORM:
    __Backends = Literal["sqlite", "mysql", "postgres"]
    __backend: DatabaseBackend
    __backend_instances ={
        "sqlite": SqliteBackend(),
        "mysql": MySQLBackend(),
        "postgres": PostgreSQLBackend()
    }
    class ConnectionParams(TypedDict, total=False): 
        host: str
        port: int
        database: str
        user: str
        password: str

    def __init__(
            self, 
            backend: DatabaseBackend | __Backends,  
            host: str,
            port: int,
            database: str,
            user: str,
            password: str):
        try:
            if isinstance(backend, DatabaseBackend):
                self.__backend = backend
            else: 
                self.__backend = self.__backend_instances[backend]

        except KeyError:
            raise ValueError(f"Invalid backend: {backend}, valid backends are: {list(self.__backen_instance.keys())}")

        self.connect(
            connection_params={
                "host": host,
                "port": port,
                "database": database,
                "user": user,
                "password": password
            }
        )

    def connect(self, connection_params: ConnectionParams,  **kwargs) -> DatabaseBackend:
        kwargs.update(connection_params)
        return self.backend.connect(**kwargs)

    def execute_query(self, query: str, params=None) -> None:
        return self.backend.execute_query(query, params)

    def fetch_all(self) -> None:
        return self.backend.fetch_all()

    def close(self) -> None:
        return self.backend.close() 
    

    def __exit__(self) -> None:
        self.backend.__exit__()


    def get_default_conection_params(self):
        return self.backend.get_default_conection_params()
    

    @property
    def backend(self) -> DatabaseBackend:
        return self.__backend
    


