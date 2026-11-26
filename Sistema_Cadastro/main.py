from db import conectar, criar_banco_e_tabela
from app import AppCadastro
if __name__ == '__main__':
    try:
        c = conectar(usar_banco=False)
        criar_banco_e_tabela(c)
        c.close()
    except Exception:
        pass
    app = AppCadastro()
    app.mainloop()
