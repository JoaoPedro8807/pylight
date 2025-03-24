from abc import ABC, abstractmethod



class DatabaseBackend(ABC):
    
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def execute_query(self, query: str, params=None):
        pass

    @abstractmethod
    def fetch_all(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_default_conection_params() -> dict:
        pass    
    @abstractmethod
    def get_sql_type(self, field_type: str, **kwargs) -> str:
        pass
    @abstractmethod    
    def get_supported_date_format(self) -> str:
        pass

    def __exit__(self):
        self.close()
