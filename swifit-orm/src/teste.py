from main.main import SwifitORM
from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField
from main.session import Session
from backend import SqliteBackend
def main():
    sqlite  = SqliteBackend(db_file="testando.db")
    #sqlite = sqlite.connect(database="test.db")
    orm = SwifitORM(
        backend=sqlite,
    )
    class Pessoa(Model):    
        id = CharField(autoincrement=True, primary_key=True, not_null=True, default="321")
        nome = CharField(length=50)
        numero = IntegerField(not_null=True)
        data = DateField(not_null=True, default="2021-10-10")
        ativo = BooleanField(not_null=True, default=True)

        

    with Session(orm) as session:
        try:
            session.create_table(model=Pessoa)
        except Exception as e:
            print(e)

    print("Tabela criada com sucesso!")
        
        

    
    

if __name__ == "__main__":
    main()