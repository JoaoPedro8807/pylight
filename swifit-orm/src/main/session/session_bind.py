from typing import TYPE_CHECKING, List, Optional, TypeVar, Type
from main.exceptions import ModelValueError
from main.filters import BaseFilter

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

    def find(self, model: Type[T], filters: Optional[List[BaseFilter]] = None,**kwargs) -> T | List[T]:
        instance = self._engine.select(model, filters=filters, **kwargs)
        return instance

    
    def add_all(self, models: list["Model"], commit: bool = True, **kwargs):
        for model in models:
            self._engine.insert(model, **kwargs)
        if commit:
            self.commit()

    def select_all(self, model: Type[T], **kwargs) -> list[T]:
        instances = self._engine.select_all(model, **kwargs)
        return instances


    def update(self, model: "Model", commit: bool = True, **kwargs):
        changes = model.get_changes()
        if not changes:
            raise ModelValueError("Nenhuma alteração encontrada para salvar.")

        model.update_original_state()

        self._engine.update(model, **kwargs)


    def delete(self, model: "Model", commit: bool = True, **kwargs):
        self._engine.delete(model, **kwargs)
        if commit:
            self.commit()


    def save(self, model: "Model", commit: bool = True, **kwargs):
        ...
       


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