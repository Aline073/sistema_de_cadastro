# Importa o módulo principal 'pymysql', que é a biblioteca usada para
#                conectar o Python ao banco de dados MySQL.
# Essa biblioteca permite executar comandos SQL (como SELECT, INSERT,
#                UPDATE, DELETE) diretamente a partir do Python.
import pymysql

# Importa o submódulo 'err' de dentro do pacote pymysql e o renomeia para 'pymysql_err'.
# facilita a leitura do código quando precisar tratar erros específicos do MySQL.
from pymysql import err as pymysql_err

# Importa do arquivo 'config.py' todas as variáveis de configuração
# necessárias para a conexão com o banco de dados.
from config import HOST, PORTA, USUARIO, SENHA, NOME_BANCO, NOME_TABELA


# Define a função 'conectar', responsável por abrir uma conexão com o banco de dados MySQL.
# O parâmetro 'usar_banco' (por padrão = True) indica se a conexão já
# deve ser feita diretamente com o banco de dados
# definido em NOME_BANCO. Caso ele ainda não exista, o
# código cria o banco e depois reconecta.
def conectar(usar_banco=True):

    try:

        # Verifica se a função deve se conectar diretamente ao banco de dados já existente.
        # Caso 'usar_banco' seja True, tenta conectar usando o nome do banco definido em NOME_BANCO.
        if usar_banco:

            # Retorna uma conexão ativa com o MySQL, configurada com as
            #                informações definidas em config.py.
            # Essa conexão é usada para executar comandos SQL em outras partes do sistema.
            return pymysql.connect(

                host=HOST,

                port=PORTA,

                user=USUARIO,

                password=SENHA,

                charset="utf8mb4",

                autocommit=True,

                # cursorclass → define o tipo de cursor usado para manipular os
                #                resultados das consultas SQL.
                # Aqui, pymysql.cursors.Cursor é usado, o que retorna os
                #                dados como tuplas (linhas de valores).
                cursorclass=pymysql.cursors.Cursor

            )

        # Caso o parâmetro 'usar_banco' seja False, o sistema se conecta apenas ao servidor MySQL,
        # sem especificar o nome do banco de dados (NOME_BANCO).
        # Isso é útil em situações em que o banco de dados ainda não existe e precisa ser criado.
        else:

            # Retorna uma conexão ativa com o servidor MySQL (sem selecionar um banco específico).
            # Essa conexão é usada, por exemplo, para executar o comando CREATE DATABASE.
            return pymysql.connect(

                host=HOST,

                port=PORTA,

                user=USUARIO,

                password=SENHA,

                charset="utf8mb4",

                autocommit=True,

                cursorclass=pymysql.cursors.Cursor

            )

    # Captura um erro específico do tipo "OperationalError", que ocorre quando há falha operacional
    # durante a tentativa de conexão ao banco de dados MySQL.
    # Exemplos de falhas: banco inexistente, servidor desligado, senha incorreta, etc.
    except pymysql_err.OperationalError as e:

        # O código de erro 1049 no MySQL significa "Unknown database" (banco de dados desconhecido),
        #                ou seja, o nome do banco definido em NOME_BANCO ainda não existe.
        # Nesse caso, o sistema cria o banco automaticamente e tenta se reconectar.
        if getattr(e, "args", None) and e.args and e.args[0] == 1049:

            # Cria uma nova conexão com o servidor MySQL,
            #                mas desta vez **sem** especificar o nome do banco (pois
            #                ele ainda não existe).
            # Essa conexão temporária é usada apenas para criar o banco e a tabela.
            conn = pymysql.connect(

                host=HOST,

                port=PORTA,

                user=USUARIO,

                password=SENHA,

                charset="utf8mb4",

                autocommit=True,

                cursorclass=pymysql.cursors.Cursor,
            )

            # Chama a função 'criar_banco_e_tabela', responsável por:
            #   1. Criar o banco de dados (caso não exista)
            #   2. Criar a tabela “pessoas” dentro do banco.
            # Essa função está definida mais abaixo neste mesmo arquivo.
            criar_banco_e_tabela(conn)

            # Fecha a conexão temporária criada apenas para montar o banco e tabela.
            # Isso é importante para liberar recursos antes de abrir uma nova conexão definitiva.

            conn.close()

            # Esse retorno final entrega uma conexão pronta para uso em todo o sistema.

            return pymysql.connect(

                host=HOST,

                port=PORTA,

                user=USUARIO,

                password=SENHA,

                database=NOME_BANCO,

                charset="utd8mb4",

                autocommit=True,

                cursorclass=pymysql.cursors.Cursor

            )

    # Se o erro capturado não for do tipo “banco inexistente” (1049),
    # o Python reenvia (raise) a exceção original, permitindo
    # que ela seja tratada em outro nível do código.
    # Isso evita suprimir erros graves (como senha incorreta, servidor desligado etc.).

    raise

# Define a função 'criar_banco_e_tabela', que recebe como parâmetro uma conexão ativa com o MySQL (conn).
# Essa função tem a responsabilidade de garantir que o banco de dados e a
# tabela necessários existam antes de o sistema começar a utilizá-los.
# Se ainda não existirem, eles serão criados automaticamente.


def criar_banco_e_tabela(conn):

    # O comando "with conn.cursor()" cria um cursor de forma temporária.
    # O cursor é o objeto que permite executar comandos SQL (como CREATE, SELECT, INSERT, etc.)
    #                dentro da conexão aberta (conn).
    # A palavra-chave "as cur" dá o nome “cur” ao cursor, facilitando seu uso dentro do bloco.
    # Ao final do bloco "with", o cursor é automaticamente fechado, mesmo se ocorrer algum erro.
    with conn.cursor() as cur:

        # Este trecho de código é o coração da criação do banco de dados.
        # Ele executa um comando SQL (Structured Query Language), que é a linguagem usada
        #               para conversar com o MySQL e manipular bancos de dados (criar,
        #               apagar, modificar, etc).
        cur.execute(

            # "IF NOT EXISTS" é uma cláusula de segurança que impede o MySQL de gerar um erro
            #                  caso o banco já exista — ele apenas ignora o
            #                  comando se o banco já estiver criado.
            # - {NOME_BANCO} é uma variável Python que é substituída dinamicamente pelo nome do banco,
            #                  por exemplo, "cadastro_db". O "f" antes das aspas indica que é
            #                  uma *f-string*, ou seja, permite inserir variáveis dentro da string.

            f"CREATE TABLE IF NOT EXISTS {NOME_BANCO}"
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
        )

        cur.execute(f"USE {NOME_BANCO};")

        cur.execute(
            f""""
            CREATE TABLE IF NOT EXISTS {NOME_TABELA}(
                id INT AUTO_INCREMENT PRIMAY KEY,
                nome_VARCHAR(120) NOT NULL,
                email_VARCHAR(150) NOT NULL,
                telefone_VARCHAR(30) NOT NULL,
                criado_em_TIMESTAMP_DEFAULT_CURRENT_TIMESTAMP
            )   ENGINE=innoDB DEFAULT CHARACTER=utf8mb4;
            """

        )
