from main.main import Pylight
from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField, TimeField, IDField
from main.session import Session
from model_teste import Pessoa
from main.filters import Eq, In, Like

def main():
    orm = Pylight(
        backend="postgres",
        host="localhost",
        port=5432,
        database="dbteste",
        user="postgres",
        password="postgres",
    )
    conn = Session(orm)

    with Session(orm) as session:
        session.create_table(Pessoa)
        nova_pessoa = Pessoa.create(
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
            print(pessoa.)














        pessoa1 = session.find(Pessoa, id=1, ativo=True)
        pessoa1.
        joao_silva = session.find(
            Pessoa, nome="joao silva", ativo=True)

        for pessoa in pessoas:
            print(pessoa.nome, pessoa.id, )

        pessoas_alteradas2 = session.find(Pessoa, nome="alterei dnv", ativo=True) # cache 


        pessoas_com_filtro = session.find(Pessoa,
            filters=[
                In({"id": [1, 2, 3]}),
                Like({"nome": "teste"})
                ])

        for pessoa in pessoas_com_filtro:
            print(pessoa.nome, pessoa.id)

        print("PRINTANDO PESSOAS ALTERADAS 2 ")
        for pessoa in pessoas_alteradas2:
            print(pessoa.nome, pessoa.id)


if __name__ == "__main__":
    main()