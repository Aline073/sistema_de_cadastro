# conectar abre uma conexão com o servidor e MySQL.
# criar_banco_e_tabela garante que o banco e a tabela necessários existam, criando os se necessário.
# essas funções são essenciais para preparar o ambiente do banco de dados antes da interface.
from db import conectar, criar_banco_e_tabela


# importa do módulo app a classe "AppCadastro".
# essa classe representa toda a interface gráfica (GUI) do sistema feita em Tkinter
# contém todos campos necessários para interação gráfica.
from app import AppCadastro


# a condição abaixo verifica se o arquivo atual está sendo executado
# e não importado por outro módulo.
# "__name__" é uma variável especial do Python:
# quando o arquivo é executado diretamente, __name__=="__main__".
# quando é importado por outro arquivo, __name__ contém o nome do módulo.
# assim, o código dentro deste bloco só será executado quando o programa for iniciado diretamente pelo usuário.
if __name__ == '__main__':
    try:
        c = conectar(usar_banco=False)

        # chama a função "criar_banco_e_tabela", passando a conexão aberta.
        # essa função cria o banco de dados (schema) e a tabela principal (pessoas) caso ainda não existen.
        criar_banco_e_tabela(c)

        # fecha a conexão  temporária usada apenas para criar o banco e a tabela,
        # Isso libera recursos dp servidor MySQL antes de abrir a conexão principal usada pela aplicação.
        c.close()

    # caso aconteça qualquer erro durante essa etapa de conesão ou criação do banco, o progrma não interrompe a execução.
    # em vez disso, o except captura a exceção silenciosamente.
    # o próprio PyMySQL imprime a mensagem de erro no console, o que ajuda na depuração.
    except Exception:

        # "pass" significa literalmente "não faça nada" - ele ignora o erro e segue a execução.
        pass

    # cria uma instância de classe "appCadastro", que representa a janela principal do programa.
    # ao ser criada, essa instÂncia monta toda a interface gráfica e conecta automaticamente ao banco já preparado.
    app = AppCadastro()

    # executa o loop principal da interface Tkinter
    # o método mainloop() mantéma janela aberta e executa as ações do usuário (como cliques e digitaçaõ).
    # ele é essencial para que o programa gráfico permaneça ativo até que o ususário o feche.
    app.mainloop()
