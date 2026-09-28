from flask import Flask, render_template, request, redirect
import sqlite3
from database import criar_banco

app = Flask(__name__)

criar_banco()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/pessoas", methods=["GET", "POST"])
def pessoas():
    if request.method == "POST":
        nome = request.form["nome"]
        idade = request.form["idade"]
        telefone = request.form["telefone"]

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO pessoas (nome, idade, telefone, data_cadastro)
            VALUES (?, ?, ?, datetime('now', 'localtime'))
        """, (nome, idade, telefone))

        conexao.commit()
        conexao.close()

        return redirect("/pessoas")

    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, idade, telefone, data_cadastro
        FROM pessoas
        ORDER BY id DESC
    """)

    pessoas = cursor.fetchall()

    conexao.close()

    return render_template("pessoas.html", pessoas=pessoas)


@app.route("/atendimentos", methods=["GET", "POST"])
def atendimentos():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    if request.method == "POST":
        pessoa_id = request.form["pessoa_id"]
        data = request.form["data"]
        tipo = request.form["tipo"]
        observacao = request.form["observacao"]

        cursor.execute("""
            INSERT INTO atendimentos
            (pessoa_id, data, tipo, observacao)
            VALUES (?, ?, ?, ?)
        """, (pessoa_id, data, tipo, observacao))

        conexao.commit()
        conexao.close()

        return redirect("/atendimentos")

    cursor.execute("""
        SELECT id, nome
        FROM pessoas
        ORDER BY nome
    """)

    pessoas = cursor.fetchall()

    cursor.execute("""
        SELECT
            atendimentos.id,
            pessoas.nome,
            atendimentos.data,
            atendimentos.tipo,
            atendimentos.observacao
        FROM atendimentos
        INNER JOIN pessoas
            ON atendimentos.pessoa_id = pessoas.id
        ORDER BY atendimentos.id DESC
    """)

    historico = cursor.fetchall()

    conexao.close()

    return render_template(
        "atendimentos.html",
        pessoas=pessoas,
        historico=historico
    )


@app.route("/dashboard")
def dashboard():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM pessoas")
    total_pessoas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM atendimentos")
    total_atendimentos = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM atendimentos
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now', 'localtime')
    """)
    atendimentos_mes = cursor.fetchone()[0]

    conexao.close()

    return render_template(
        "dashboard.html",
        total_pessoas=total_pessoas,
        total_atendimentos=total_atendimentos,
        atendimentos_mes=atendimentos_mes
    )


if __name__ == "__main__":
    app.run(debug=True)