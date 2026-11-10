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

    # Inicia o bloco try/except para capturar e tratar possíveis erros de conexão,
    # como falha na autenticação, servidor MySQL desligado ou banco inexistente.
    try:

        # Verifica se a função deve se conectar diretamente ao banco de dados já existente.
        # Caso 'usar_banco' seja True, tenta conectar usando o nome do banco definido em NOME_BANCO.
        if usar_banco:

            # Retorna uma conexão ativa com o MySQL, configurada com as
            # informações definidas em config.py.
            # Essa conexão é usada para executar comandos SQL em outras partes do sistema.
            return pymysql.connect(

                host=HOST,  # endereço do servidor MySQL

                port=PORTA,  # porta de comunicação usada pelo MySQL

                user=USUARIO,  # nome do usuário autorizado a acessar o banco de dados

                password=SENHA,  # senha do usuário definida no servidor MySQL

                # nome do banco de dados que será acessado (ex.: 'cadastro_db')
                database=NOME_BANCO,

                # define a codificação de caracteres usada para armazenar textos.
                charset="utf8mb4",
                # utf8mb4 é uma versão aprimorada do UTF-8, que suporta
                # emojis e todos os caracteres especiais.

                autocommit=True,  # faz com que cada comando SQL seja confirmado automaticamente
                                 # sem precisar chamar conn.commit() manualmente após cada operação.


                # cursorclass → define o tipo de cursor usado para manipular os
                cursorclass=pymysql.cursors.Cursor
                # resultados das consultas SQL.
                # Aqui, pymysql.cursors.Cursor é usado, o que retorna os
                # dados como tuplas (linhas de valores).

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
            # mas desta vez sem especificar o nome do banco (pois
            # ele ainda não existe).
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
            # 1. Criar o banco de dados (caso não exista)
            # 2. Criar a tabela “pessoas” dentro do banco.
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
    # dentro da conexão aberta (conn).
    # A palavra-chave "as cur" dá o nome “cur” ao cursor, facilitando seu uso dentro do bloco.
    # Ao final do bloco "with", o cursor é automaticamente fechado, mesmo se ocorrer algum erro.
    with conn.cursor() as cur:

        # O trecho abaixo é o coração da criação do banco de dados.
        # Ele executa um comando SQL (Structured Query Language), que é a linguagem usada
        # para conversar com o MySQL e manipular bancos de dados (criar,
        #  apagar, modificar, etc).

        # f"CREATE DATABASE IF NOT EXISTS {NOME_BANCO}"
        # - "CREATE DATABASE" é um comando SQL que cria um novo banco de dados.
        # - "IF NOT EXISTS" é uma cláusula de segurança que impede o MySQL de gerar um erro
        # caso o banco já exista — ele apenas ignora o
        # comando se o banco já estiver criado.
        # - {NOME_BANCO} é uma variável Python que é substituída dinamicamente pelo nome do banco,
        # por exemplo, "cadastro_db". O "f" antes das aspas indica que é
        #                  uma *f-string*, ou seja, permite inserir variáveis dentro da string.

        # ▶ "DEFAULT CHARACTER SET utf8mb4"
        # - "CHARACTER SET" define qual conjunto de caracteres será usado para armazenar textos no banco.
        # - "utf8mb4" é uma codificação moderna e completa que suporta todos os caracteres Unicode,
        # incluindo acentos (como á, ê, ç) e até emojis (😀🔥❤️).
        # Usar utf8mb4 evita problemas de caracteres “bugados” quando se insere textos com acentos.

        # "COLLATE utf8mb4_general_ci"
        # - "COLLATE" define as regras de *comparação* e *ordenação* de textos.
        # - "utf8mb4_general_ci" significa:
        # “utf8mb4” → mesmo conjunto de caracteres do CHARSET.
        # “general” → tipo de regra geral de ordenação.
        # “ci” → *case insensitive*, ou seja, ignora diferença entre maiúsculas e minúsculas.

        # Em resumo, esse comando cria o banco de dados com suporte a todos os
        # caracteres e comparações amigáveis, o que é essencial para
        # aplicativos em português.

        # O método .execute() envia o comando SQL ao servidor MySQL através do cursor “cur”.
        # O MySQL interpreta a string e executa o comando, criando fisicamente o banco no servidor.

        cur.execute(

            f"CREATE TABLE IF NOT EXISTS {NOME_BANCO}"
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
        )

        # Em seguida, executa o comando SQL "USE", que seleciona o banco de dados recém-criado
        # (ou existente) para que os próximos comandos SQL sejam executados dentro dele.
        # Esse comando é obrigatório antes de criar tabelas, pois o MySQL precisa saber
        # em qual banco de dados a tabela será criada.

        cur.execute(f"USE {NOME_BANCO};")

        # ▶ f""" ... """
        # - O prefixo “f” indica que é uma *f-string*, permitindo inserir variáveis
        # Python diretamente no texto SQL.
        # - As três aspas """ """ permitem escrever o comando SQL em múltiplas
        # linhas, deixando o código mais legível.
        # - {NOME_TABELA} será substituído pelo nome definido na variável (ex.: “pessoas”).

        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {NOME_TABELA}(
                id INT AUTO_INCREMENT PRIMAY KEY, 
                nome_VARCHAR(120) NOT NULL,
                email_VARCHAR(150) NOT NULL,
                telefone_VARCHAR(30) NOT NULL,                                               
                criado_em_TIMESTAMP_DEFAULT_CURRENT_TIMESTAMP 
                   )   ENGINE=innoDB DEFAULT CHARACTER=utf8mb4;
            """
            # - “DEFAULT CURRENT_TIMESTAMP” faz com que o MySQL insira automaticamente a data e hora
            # no momento em que o registro é criado.
            # Assim, o sistema sempre saberá quando cada cadastro foi feito.

            # ENGINE=InnoDB
            # - “ENGINE” indica o tipo de mecanismo de armazenamento usado pelo MySQL.
            # - “InnoDB” é o mais moderno e seguro, suportando transações e chaves estrangeiras

        )
