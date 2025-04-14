from main.main import SwifitORM
from main.model import Model
from main.model.fields import CharField, IntegerField, DateField, BooleanField, TimeField, IDField
from main.session import Session
def main():
    orm = SwifitORM(
        backend="postgres",
        host="localhost",
        port=5432,
        database="dbteste",
        user="postgres",
        password="postgres",
    )
    class Pessoa(Model):  
        id = IDField(auto_increment=True)
        nome = CharField(length=50)
        numero = IntegerField(not_null=True)
        data = DateField(not_null=True) # date != datetime != time
        ativo = BooleanField(not_null=True, default=True)

    with Session(orm) as session:
        session.create_table(Pessoa)
        pessoa = Pessoa.create(
            nome="teste1232",
            data="2021-10-10",
            ativo=True,
            numero=10
        )   
        pessoa.save(session=session)


if __name__ == "__main__":
    main()