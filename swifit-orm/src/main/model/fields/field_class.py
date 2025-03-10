
class Field:
    """
    Classe base para campos de modelo.
    """

    _MAX_LENGTH = 255

    def __init__(self, **kwargs):
        self.options = kwargs

    def __str__(self):
        return str(self.options)