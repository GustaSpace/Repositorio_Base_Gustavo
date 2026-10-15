from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

nome_banco = 'cadastro.db'


script_tabela = """CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password NOT NULL
            );"""
            

try:
    with sqlite3.connect(nome_banco) as conn:
        # Cria um cursor
        cur = conn.cursor()

        # Executa o script
        cur.execute(script_tabela)

        # Salva as alterações no banco de dados
        conn.commit()

        print("Tabelas Criadas com Sucesso")
except sqlite3.OperationalError as e:
    print("ERRO: ", e)

def cadastrar_usuario(nome, email, senha):
     script_cadastrar = "INSERT INTO usuario (username, email, password) VALUES (?,?,?)"

     try:
            with sqlite3.connect(nome_banco) as conn:
                # Cria um cursor
                cur = conn.cursor()

                # Executa o script
                cur.execute(script_cadastrar,(nome, email, senha))

                # Salva as alterações no banco de dados
                conn.commit()

     except sqlite3.OperationalError as e:
            print("ERRO: ", e)

def consultar_usuario(username):
    script_consulta_usuario = """ SELECT * FROM usuario WHERE username = ?"""
    try:
        with sqlite3.connect(nome_banco) as conn:
            conn.row_factory = sqlite3.Row

            # Cria um cursor
            cur = conn.cursor()

            # Executa a consulta
            cur.execute(script_consulta_usuario, (username,))

            # Pega o primeiro resultado
            res = cur.fetchone()

            return res
    except sqlite3.OperationalError as e:
        print("ERRO:", e)

def validar_login(usuario, senha):
    resultado_consulta = consultar_usuario(usuario)
    if resultado_consulta:
        return check_password_hash(resultado_consulta['password'], senha)
    else:
        return False