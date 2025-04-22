from backend import DatabaseBackend
from typing import Literal, TypedDict, Optional, List
from backend import SqliteBackend, MySQLBackend, PostgreSQLBackend 
from .exceptions import SwifitORMException
from main.filters import BaseFilter
from .model import Model
from pathlib import Path

class SwifitORM:
    Backends = Literal["sqlite", "mysql", "postgres"]
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
            backend: DatabaseBackend | Backends,  
            host: str = None,
            port: int = None,
            database: str = None,
            user: str = None,
            password: str = None,
            db_file: str | Path = None # only for sqlite
            ):
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
                "password": password,
            }
        )

    def connect(self, connection_params: ConnectionParams,  **kwargs) -> DatabaseBackend:
        kwargs.update(connection_params)
        return self.backend.connect(**kwargs)

    def execute_query(self, query: str, params=None) -> None:                                                   
        return self.backend.execute_query(query, params)
    
    def commit(self) -> None:
        return self.backend.commit()

    def select(self, model: Model, filters: Optional[List[BaseFilter]], **kwargs) -> Model:
        return self.backend.select(model=model, filters=filters, **kwargs)

    def select_all(self, model: Model) -> None:
        return self.backend.select_all(model=model)

    def close(self) -> None:
        return self.backend.close() 
    
    def create_table(self, model: Model) -> None:
        #verificar validação do model
        return self.backend.create_table(model)
    
    def update(self, model: Model, **kwargs) -> None:
        model.validate_all(backend=self.backend)
        return self.backend.update(model, **kwargs)

    def insert(self, model: Model, **kwargs) -> None:
        model.validate_all(backend=self.backend)
        return self.backend.add(model, **kwargs)
    
    def delete(self, model: Model, **kwargs) -> None:
        model.validate_all(backend=self.backend)
        return self.backend.delete(model, **kwargs)

            
    def __exit__(self) -> None: 
        self.backend.__exit__()


    def get_default_conection_params(self):
        return self.backend.get_default_conection_params()
    

    @property
    def backend(self) -> DatabaseBackend:
        return self.__backend
    


