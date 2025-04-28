from compilers import SQLCompiler
from main.cache import PylightCache

class DbBase:
    def __init__(self):
        self._compiler = SQLCompiler()
        self.__cache = PylightCache() # talvez normalizar isso e as outras coisas que se repetem em backends em outra classe

    @property
    def compiler(self):
        return self._compiler
    
    @property
    def cache_manager(self):
        return self.__cache
