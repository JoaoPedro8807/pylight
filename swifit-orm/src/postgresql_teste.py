from main.main import SwifitORM
from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField, TimeField, IDField
from main.session import Session
from model_teste import Pessoa
from main.filters import Eq, In

def main():
    orm = SwifitORM(
        backend="postgres",
        host="localhost",
        port=5432,
        database="dbteste",
        user="postgres",
        password="postgres",
    )

    with Session(orm) as session:
        session.create_table(Pessoa)
        pessoa = Pessoa.create(
            nome="teste1232",
            data="2021-10-10",
            ativo=True,
            numero=10
        )   
        session.add(pessoa, commit=True)
        pessoa.nome = "alterei dnv"
        
        session.update(pessoa, commit=True)
        pessoas = session.select_all(Pessoa)
        for pessoa in pessoas:
            print(pessoa.nome)

        pessoas_alteradas = session.find(Pessoa, filters=[
            Eq({
            "nome": "alterei dnv",
            }), In({
                "id": [30, 32]
            })
    ])
        for pessoa in pessoas_alteradas:
            print(pessoa.nome, pessoa.id)




if __name__ == "__main__":
    main()