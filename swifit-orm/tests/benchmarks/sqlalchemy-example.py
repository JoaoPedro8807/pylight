from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Criando a base para os modelos
Base = declarative_base()

# Definindo um modelo de Livro
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

# Criando a conexão com o banco de dados
engine = create_engine("sqlite:///books.db")

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Criando as tabelas no banco
Base.metadata.create_all(engine)
