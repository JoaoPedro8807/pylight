from main.main import SwifitORM
from main.session import Session
from model_teste import Pessoa

orm = SwifitORM(
    backend="postgres",
    host="localhost",
    port=5432,
    database="dbteste",
    user="postgres",
    password="postgres",
)

with Session(orm) as sessao:
    sessao.create_table(Pessoa)


nova_pessoa = Pessoa.create(
    nome="UsuarioTeste",
    data="2021-10-10",
    ativo=True,
    numero=10
)
sessao.add(nova_pessoa, commit=True)


# Alteração local no objeto em memória
nova_pessoa.nome = "UsuarioAtualizado"

# Persistência da alteração no banco
sessao.update(nova_pessoa, commit=True)


pessoas = sessao.select_all(Pessoa)
for pessoa in pessoas:
    print(pessoa.nome)

# Consulta utilizando parâmetros diretos
pessoas_filtradas = sessao.find(Pessoa, nome="UsuarioAtualizado", ativo=True)

# Consulta utilizando filtros compostos
from main.filters import In, Like

pessoas_avancadas = sessao.find(
    Pessoa,
    filters=[
        In({"id": [1, 2, 3]}),
        Like({"nome": "Usuario"})
    ]
)    