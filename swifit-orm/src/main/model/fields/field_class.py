
class Field:
    """
    Classe base para campos de modelo.
    """
    def __init__(self, **kwargs):
        self.options = kwargs

    def __str__(self):
        return str(self.options)