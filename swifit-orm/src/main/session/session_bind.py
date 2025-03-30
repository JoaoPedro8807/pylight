from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..main import SwifitORM
    from main.model.base.model_base import Model



class Session:
    _engine: 'SwifitORM' = None

    def __init__(self, orm_engine: 'SwifitORM'):
        self._engine = orm_engine


    def add(self, model: "Model", **kwargs):
        self._engine.insert(model, **kwargs)

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