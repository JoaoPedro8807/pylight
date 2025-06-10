# ORGANIZAÇÃO:
### introdução / problemática
    1 - impedance mismatch / mapeamento
    2 - como funciona o orm classes/tabelas
    3 - VANTANGES: centralização das regras e desacoplamento


### referencial 
    4 - 


### metodologia 
    5 - 
    6 -


### resultados 
    7 - 
    8 - 


# conclusao e perspectiva de continuidade
    9 -



# APRESENTAÇÃO 


### Boa noite



### Introdução:

    1 (motivação).

    Bom, antes de começara a falar sobre o ORM desse artigo, irei falar um pouco sobre a motivação da criação dos ORMs.

    Um dos principais problemas que motivou a criação de ORMs foi o Object-Relational Impedance, um conceito amplamente discutido na literatura da área. Este termo descreve a diferença entre a forma como os dados são tratados em linguagens de programação orientadas a objetos (onde se trabalha com objetos que encapsulam dados e comportamento, representando entidades do mundo real) e a forma como são armazenados em bancos de dados relacionais (que utilizam tabelas, linhas e colunas para organizar os dados).

    Apesar de bancos de dados possuem relacionamentos entre tabelas, ainda sim pode não conseguir representar todas as funcionalidades de uma Entidade. Por exemplo, nessa imagem, imagine que uma entidade usuario tenha que ter esses métodos de resgatar o nome e registrar. Isso na linguagem de programação seria uma tarefa simples, mas seria muito mais complexo fazer a mesma função em SGBDs relacionais, daí que surge a ideia do ORM. Claro, isso é apenas um exemplo simples, orms geralmente lidam com problemas mais complexos.
    
    
    Para resolver isso, os ORMs atuam como uma ponte: mapeiam objetos do código da linguagem para tabelas do banco de dados. Ou seja, a cada novo objeto da aplicação (seja ela, web, desktop, automação), esse novo objeto terá sua respectiva referencia no SGBD. Da mesma forma, ao converter dados do banco em objetos para uso na aplicação, o desenvolvedor tem consigo não apenas os dados, mas também todas as funcionalidades (métodos) que estão esse objeto possúi. Assim, gerenciando todo o ciclo de vida dos dados de forma transparente para o desenvolvedor, que interage apenas com os objetos da linguagem de programação.


    2 (como é feito). 

    E como realmente o ORM faz isso ? Bom, basicamente orms trabalham com classes Modelos que representam tabelas reais no SGBD, e objetos dessa classe serão novas linhas da respectiva tabela. Seus campos definidos na sua classe viram colunas na tabelas, esses campos além de representar tipos primitivos diferentes (seja inteiro, varchar, date), também podem receber parâmetros para validação, como tamanho máximo, valor padrão entre outros.

    Já na busca de dados, o acesso fica bem mais fácil e entuitivo, já que utilizando atributos e métodos do objeto, temos suas informações sem a necessidade de escrever o SQL.




3.
    
    Além disso, os orms consegue fazer com que aplicações centralize as regras de negócio e as funcionalidades da aplicação apenas no código da linguagem, deixando desenvolvimento mais rápido, mais fácil de fazer manutenção/alterações, e desacoplado ao um SGBD específico, já que ele consegue mapear para diferentes SGBDs. 



