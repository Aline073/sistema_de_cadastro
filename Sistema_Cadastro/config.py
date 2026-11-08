# Configurações do Banco

# Define a constante HOST, que indica o endereço do servidor de banco de dados MySQL.
# "localhost" significa que o banco está sendo executado na mesma máquina onde o programa está rodando.
# Caso o banco estivesse em outro computador, seria necessário informar o IP ou o
#                domínio, como "192.168.0.10" ou "meuservidor.com".
HOST = "localhost"

# Define a constante PORTA, que representa a porta de comunicação usada para acessar o servidor MySQL.
# O valor padrão do MySQL é 3306. Caso o servidor use outra porta, ela deve ser ajustada aqui.
PORTA = 3306

# Define a constante USUARIO, que indica o nome do usuário do banco de dados.
# Esse usuário precisa ter permissão de leitura e escrita para o banco definido.
# Aqui o usuário é “root”, que é o administrador principal do MySQL.
USUARIO = "root"

# Define a constante SENHA, que contém a senha de acesso ao banco de dados MySQL.
# É essencial que a senha corresponda exatamente à configurada no MySQL do computador.
# No caso deste projeto, a senha é “$Aluno123BD”.
SENHA = "$Aluno123BD"

# Define o nome do banco de dados (schema) que será utilizado pelo aplicativo.
# O banco de dados “cadastro_db” armazenará a tabela “pessoas”.
# Se esse banco ainda não existir, o código Python criará ele
#                automaticamente na primeira execução.
NOME_BANCO = "cadastro_db"

# Define o nome da tabela dentro do banco de dados que armazenará os registros de pessoas.
# A tabela “pessoas” conterá as colunas ID, Nome, E-mail, Telefone e Data de Criação.
# Esse nome é utilizado em diversas partes do código, como nas
#                instruções SQL (SELECT, INSERT, UPDATE, DELETE).
NOME_TABELA = "pessoas"
