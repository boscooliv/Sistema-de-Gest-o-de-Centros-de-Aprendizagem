import sqlite3

DB_PATH = "tarefas.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL,
                curso TEXT NOT NULL
            )
        """)
        conn.commit()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                area TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS centros (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                local TEXT NOT NULL,
                vagas INTEGER NOT NULL,
                descricao TEXT NOT NULL          
        )
        """)
        conn.commit()

