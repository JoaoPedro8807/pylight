from base import ModelBase

class Teste:
    pass


class SwifitModel(Teste, metaclass=ModelBase):
    pass



SwifitModel()