from ..base_filter import BaseFilter
class CompositerFilter(BaseFilter):
    """
    CompositerFilter is a class that allows
    """

    def __init__(self, filters: list[BaseFilter]):
        self.filters = filters

    def apply(self, query: str) -> str:
        for filter in self.filters:
            query = filter.apply(query)
        return query