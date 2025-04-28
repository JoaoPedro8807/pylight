from main.filters.base_filter import BaseFilter

class Like(BaseFilter):
    def __init__(self, filters: dict):
        self.filters = filters  
        super().__init__(filters)
        