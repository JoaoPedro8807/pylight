from main.main import SwifitORM
from main.model import Model
from main.model.fields import CharField
from main.session import Session
from backend import SqliteBackend
def main():
    print("iniciando teste")
    sqlite  = SqliteBackend(db_file="test.db")
    #sqlite = sqlite.connect(database="test.db")
    orm = SwifitORM(
        backend=sqlite,
    )
    class Pessoa(Model):
        id = CharField(autoincrement=True, primary_key=True)
        nome = CharField(length=50)

    with Session(orm) as session:
        session.create_table(Pessoa)

    print("Tabela criada com sucesso!")
        
        

    
    

if __name__ == "__main__":
    main()