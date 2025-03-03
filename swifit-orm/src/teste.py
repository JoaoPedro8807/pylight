import pandas as pd
from pydantic import BaseModel
class Teste(BaseModel):
    nome: str




teste: Teste = Teste(nome="1.4")
print(teste.nome)
    









if __name__ == '__main__':
    print("Hello World!")


