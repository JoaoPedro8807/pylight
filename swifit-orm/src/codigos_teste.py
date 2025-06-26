import csv
import datetime
from main.main import Pylight
from main.session import Session
from model_teste import Pessoa





orm = Pylight(
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
        numero=10)

    sessao.add(nova_pessoa, commit=True)


# Alteração local no objeto em memória
nova_pessoa.nome = "UsuarioAtualizado"

# Persistência da alteração no banco
sessao.update(nova_pessoa, commit=True)

from main.filters import In, Like

pessoas = sessao.select_all(Pessoa)
for pessoa in pessoas:
    print(pessoa.nome)
    


pessoas_filtradas = sessao.find(Pessoa, nome="UsuarioAtualizado", ativo=True, data=date(2021, 10, 10))


pessoas_filtradas = sessao.find(
    Pessoa, filters=[
        In({"id": [1, 2, 3]}),
        Like({"nome": "Usuario"})
    ]
)    





usuario1 = User(
    id=1,
    nome="João",
    data="2021-10-10",
    ativo=True,
)

user = User(1, "João", True)
user.enviar_email()
user.alterar_senha("nova_senha")
user.desativar()
user.autenticar()
user.obter_endereco()
user.notificar("Olá, João!")

def jsonify():
    pass

class Cliente():
    def create():
        pass


class Produto():
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def to_json(self):
        return {
            "nome": self.nome,
            "preco": self.preco
        }
class Session():
    def bulk_add(self, model, data, commit=True):
        # Simula a adição em lote de dados
        print(f"Adicionando {len(data)} registros de {model.__name__} em lote.")
        if commit:
            print("Alterações salvas no banco de dados.")    
sessao = Session()

##TESTE DE API



@app.route('/api/usuarios',) # type: ignore
def criar_usuario():
    data = request.json # type: ignore
    novo_usuario = Pessoa.create(
        nome=data['nome'],
        numero=data['numero'],
        data=data['data'],
        ativo=data['ativo'],
    )
    sessao.add(novo_usuario, commit=True)
    return jsonify(novo_usuario.to_json()) 


def cadastrar_produto():
    produtos = [
        {"nome": "Caneta", "preco": 1.99},
        {"nome": "Caderno", "preco": 15.90},
        {"nome": "Borracha", "preco": 0.99}
    ]
    sessao.bulk_add(Produto, produtos, commit=True)



def importar_clientes(arquivo_csv):
    file = open(arquivo_csv, 'r', encoding='utf-8')
    leitor = csv.DictReader(file)
    
    for linha in leitor:
        cliente = Cliente.create(
            nome=linha['Nome'],
            email=linha['Email'],
            telefone=linha['Telefone'],
            data_cadastro=datetime.now()
        )
        sessao.add(cliente, commit=True)
    print(f"{len(leitor)} clientes importados!")