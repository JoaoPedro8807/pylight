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
        data = DateField(not_null=True, default="2021-10-10")
        ativo = BooleanField(not_null=True, default=True)
        hora = TimeField(not_null=True, default="10:10:10")

    with Session(orm) as session:
        try:
            session.create_table(model=Pessoa)
            session.commit()
            pessoa = Pessoa.create(
                session=session,
                data="2021-10-10",
                hora="10:10:10",
                numero=10
            )
            pessoa.save()
            print("Pessoa criada com sucesso!")

        except Exception as e:
            print("erro no teste: ", e)


if __name__ == "__main__":
    main()