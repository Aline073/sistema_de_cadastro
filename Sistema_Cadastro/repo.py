from typing import List, Tuple

from config import NOME_TABELA


class PessoaRepo:

    # inicializando o objeto, definindo seus atributos iniciais.
    #

    def __init__(self, conn):

        self.conn = conn
        self.cur = conn.cursor()

    def inserir(self, nome: str, email: str, telefone: str) -> None:

        self.cur.execute(
            f"INSERT INTO {NOME_TABELA} (nome, email, telefone) VALUES (%s,%s,%s)",

            (nome, email, telefone),
        )

    def listar_todos(self) -> List[Tuple]:

        self.cur.execute(
            f"SELECT id, nome, email, telefone, criado_em"
            f"FROM {NOME_TABELA} ORDER BY id Desc"
        )

        return self.cur.fetchall()  # método fetchall recupera todas a linhas

    # respo
    def pequisar(self, termo: str) -> List[Tuple]:

        like = f"%{termo}%"

        self.cur.execute(
            f"""
            SELECT id, nome, email, telefone, criado_em
            FROM {NOME_TABELA}
            WHERE nome LIKE %s OR email LIKE %s OR telefone LIKE %s
            ORDER BY id DESC
            """,

            (like, like, like),
        )

        return self.cur.fetchall()  # métodpd recupera todads a linhas encontradas na consulta,

    def atualizar(self, id_: int, nome: str, email: str, telefone: str) -> None:
        self.cur.execute(
            f"UPDATE{NOME_TABELA} SET nome=%s, email=%s, telefone=%s WHERE id=%s",

            (nome, email, telefone, id_),
        )

    def excluir(self, id_: int) -> None:

        self.cur.execute(

            f"DELETE FROM {NOME_TABELA} WHERE id=%s",

            (id_,)

        )
