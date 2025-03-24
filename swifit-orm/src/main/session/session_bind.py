from typing import TYPE_CHECKING
from main.model.base.model_base import Model

if TYPE_CHECKING:
    from ..main import SwifitORM


class Session:
    _engine = None

    def __init__(self, orm_engine: 'SwifitORM'):
        self._engine = orm_engine


    def create_table(self, model: Model):
        self._engine.create_table(model)

    @property
    def engine(self) -> 'SwifitORM':
        return self._engine
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self._engine.close()