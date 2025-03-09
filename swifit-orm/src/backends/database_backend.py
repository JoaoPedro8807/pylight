from abc import ABC, abstractmethod
from typing import TypedDict, TYPE_CHECKING


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
        
    def __exit__(self):
        self.close()
