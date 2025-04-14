from main.session import Session
from backend import SqliteBackend
from main.main import SwifitORM
from model_teste import Pessoa

def main():
    sqlite  = SqliteBackend(db_file="testando.db")
    orm = SwifitORM(backend=sqlite)

    with Session(orm) as session:
        session.create_table(model=Pessoa)
        pessoa = Pessoa.create(
            session=session,
            id=1,
            nome="teste",
            data="2021-10-10",
            ativo=True,
            numero=10
        )
        pessoa.save(session=session)

def mysql():
    orm = SwifitORM(
        backend="mysql",
        host="localhost",
        port=3306,
        database="dbteste",
        user="root",
        password="root",    
    )

    with Session(orm) as session:
        session.create_table(model=Pessoa)
        pessoa = Pessoa.create(
            nome="teste",
            data="2021-10-10",
            ativo=True,
            numero=10
        )
        session.add(pessoa, commit=True)
        pessoas = session.select_all(Pessoa)
        for pessoa in pessoas:
            pessoa.data = "2021-10-11"
            # ver o mapeamento e detecção de mudanças
            session.save(pessoa, commit=True)
            print(pessoa.data)
            




        



    

if __name__ == "__main__":
    #main()
    mysql()