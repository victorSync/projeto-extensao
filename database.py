import sqlite3


def criar_banco():
    conexao = sqlite3.connect("database.db")

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            telefone TEXT,
            data_cadastro TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pessoa_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            observacao TEXT,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")