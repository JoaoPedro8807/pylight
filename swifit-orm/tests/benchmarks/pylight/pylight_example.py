from src.main.model import Model
from src.main.model.fields import CharField, IntegerField, DateField, BooleanField, IDField
from src.main.session import Session
from src.main import Pylight

class Book(Model):
    __tablename__ = "books"

    id = IntegerField(auto_increment=True, primary_key=True)
    title = CharField(length=100, not_null=True)
    author = CharField(length=100, not_null=True)


def create_table(db_file: str):
    # Criando a conexão com o banco de dados
    db = Pylight(
        backend="sqlite",
        db_file=db_file,
    )
    
    with Session(db) as session:
        try:
            print("Creating table...")
            session.create_table(Book)

        except Exception as e:
            print(f"Error creating table: {e}")

