from main.filters.base_filter import BaseFilter
from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from main.model.base.model_base import Model

class Like(BaseFilter):
    def __init__(self, filters: dict):
        self.filters = filters  
        super().__init__(filters)

    def to_sql(self, model: "Model") -> str:
        self.model = model
        self.validate_fields()
        sql = ""
        for field, value in self.filters.items():
            if isinstance(value, str):
                sql += f"{field} LIKE '%{value}%'"
            else:
                raise ValueError(f"Valor para o campo '{field}' deve ser uma string.")
        return sql
        