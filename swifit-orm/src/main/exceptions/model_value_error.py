class ModelValueError(ValueError):
    def __init__(self, msg: str,  *args):
        super().__init__(f"ModelValueError: {msg}" *args)

    def __str__(self):
        return self.args[0] if self.args else "ModelValueError: Unknown error"