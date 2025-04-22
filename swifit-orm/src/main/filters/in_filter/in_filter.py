from ..base_filter import BaseFilter
from typing import TYPE_CHECKING, Dict, List, Any
if TYPE_CHECKING:
    from main.model.base.model_base import Model

class In(BaseFilter):
    """
    Classe que representa um filtro IN.
    ## @param filters: Dicionário de filtros.

    ### ONDE: 
        {field: [value1, value2, ...]}.
    """   
    def __init__(self, filters: Dict[str, List[Any]]):
        self.filters = filters
        super().__init__(filters)

    def to_sql(self, model: "Model") -> str:
        self.model = model
        self.validate_fields()
        sql = ""
        for field, values in self.filters.items():
            sql += f"{field} IN ({', '.join(['%s'] * len(values))})"
        print("LIST DE VALUES: ", self.filters.values(), type(self.filters.values()))
        values = self.filters.values()  
        list_values = next(iter(values))  
        return sql, list_values

