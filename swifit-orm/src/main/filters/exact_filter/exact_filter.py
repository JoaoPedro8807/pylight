from ..base_filter import BaseFilter
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from main.model.base.model_base import Model

class Eq(BaseFilter):
    """
    Classe que representa um filtro EXACT.

    ## @param filters: Dicionário de filtros.

    ### ONDE: 
        {field: value}.

    """
    
    def __init__(self, filters: Dict[str, Any]):
        super().__init__(filters)

    def to_sql(self, model: "Model") -> tuple[str, list[Any]]:
        self.model = model
        self.validate_fields()
        conditions = [f"{field} = %s" for field in self.filters.keys()]
        return " AND ".join(conditions), list(self.filters.values())

