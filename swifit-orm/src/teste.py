from main.main import SwifitORM
from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField, IDField
from main.session import Session
from backend import SqliteBackend
def main():
    sqlite  = SqliteBackend(db_file="testando.db")
    #sqlite = sqlite.connect(database="test.db")
    orm = SwifitORM(
        backend=sqlite,
    )
    class Pessoa(Model):    
        id = IDField(auto_increment=True)
        nome = CharField(length=50)
        numero = IntegerField(not_null=True)
        data = DateField(not_null=True, default="2021-10-10")
        ativo = BooleanField(not_null=True, default=True)

    with Session(orm) as session:
        try:
            session.create_table(model=Pessoa)
            pessoa = Pessoa.create(
                session=session,
                id=1,
                nome="teste",
                data="2021-10-10",
                numero=10
            )
            pessoa.save()
            print("Tabela criada com sucesso!")


        except Exception as e:
            print(e)

        
        

    
    

if __name__ == "__main__":
    main()