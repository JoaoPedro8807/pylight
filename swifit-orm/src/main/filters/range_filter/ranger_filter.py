from typing import TYPE_CHECKING
from main.filters.base_filter import BaseFilter

if TYPE_CHECKING:
    from main.model.base.model_base import Model

from main.model.base.model_base import Model
class RangeFilter(BaseFilter):
    def __init__(self, filters: dict, model: "Model" = None):
        super().__init__(filters)
        self.model = model