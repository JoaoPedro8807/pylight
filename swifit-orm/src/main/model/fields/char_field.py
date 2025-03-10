from .field_class import Field
class CharField(Field):
    """
    Campo de texto.
    """
    def __init__(self, length=255, **kwargs):
        super().__init__(**kwargs)

    pass