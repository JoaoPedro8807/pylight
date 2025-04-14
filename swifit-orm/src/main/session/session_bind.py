from typing import TYPE_CHECKING, TypeVar, Type
from main.exceptions import ModelValueError

if TYPE_CHECKING:
    from ..main import SwifitORM
    from main.model.base.model_base import Model


T = TypeVar('T', bound='Model')

class Session:
    _engine: 'SwifitORM' = None

    def __init__(self, orm_engine: 'SwifitORM'):
        self._engine = orm_engine


    def add(self, model: "Model", commit: bool = True, **kwargs):
        self._engine.insert(model, **kwargs)
        if commit:
            self.commit()


    def add_all(self, models: list["Model"], commit: bool = True, **kwargs):
        for model in models:
            self._engine.insert(model, **kwargs)
        if commit:
            self.commit()

    def select_all(self, model: Type[T], **kwargs) -> list[T]:
        rows = self._engine.select_all(model, **kwargs)
     
        cursor = self._engine.backend.cursor
        if not cursor:
            raise ModelValueError("Cursos não encontrado. Verifique a conexão com o banco de dados.")
        
        instances = self._engine.backend.deseriallize(rows, model)
        

        return instances


    def create_table(self, model: "Model"):
        self._engine.create_table(model)

    def commit(self):
        self._engine.commit()

    @property
    def engine(self) -> 'SwifitORM':
        return self._engine
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._engine.close()