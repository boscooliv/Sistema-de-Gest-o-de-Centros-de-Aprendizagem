#teste git
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import List
import uuid

from database import get_conn, init_db
from models import Aluno, AlunoEntrada, Professor, ProfessorEntrada, Centro, CentroEntrada

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="API Gestão de Centros de Aprendizagem", version="2.0.0", lifespan=lifespan)

# METODOS POST!!

@app.post("/Alunos", response_model=Aluno, status_code=201)
def criar_aluno(dados: AlunoEntrada):
    aluno_id = str(uuid.uuid4())
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO alunos (id, nome, matricula, curso) VALUES (?, ?, ?, ?)",
            (aluno_id, dados.nome, dados.matricula, dados.curso)
        )
        conn.commit()
    return Aluno(id=aluno_id, **dados.model_dump())

@app.post("/Professores",response_model=Professor, status_code=201)
def criar_professor(dados: ProfessorEntrada):
    professor_id = str(uuid.uuid4())
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO professores (id, nome, area) VALUES (?, ?, ?)",
            (professor_id, dados.nome, dados.area)
        )
        conn.commit()
    return Professor(id=professor_id, **dados.model_dump())

@app.post("/Centros", response_model=Centro, status_code=201)
def criar_centro(dados: CentroEntrada):
    centro_id = str(uuid.uuid4())
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO centros (id, data, local, vagas, descricao) VALUES (?, ?, ?, ?, ?)",
            (centro_id, dados.data, dados.local, dados.vagas, dados.descricao)
        )
        conn.commit()
    return Centro(id=centro_id, **dados.model_dump())

# MÉTODOS DE CONSULTA!!

@app.get("/Alunos", response_model=List[Aluno])
def listar_alunos():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, nome, matricula, curso FROM alunos"
        ).fetchall()
    return [Aluno(id=r["id"], nome=r["nome"], matricula=r["matricula"], curso=r["curso"]) for r in rows]

@app.get ("/Professores", response_model=List[Professor])
def listar_professores():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, nome, area FROM professores"
        ).fetchall()
    return [Professor(id=r["id"], nome=r["nome"], area=r["area"])for r in rows]

@app.get ("/Centros", response_model=List[Centro])
def listar_centros():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, data, local, vagas, descricao FROM centros"
        ).fetchall()
    return [Centro(id=r["id"], data=r["data"], local=r["local"], vagas=r["vagas"], descricao=r["descricao"]) for r in rows]


@app.get("/Alunos/{id}", response_model=Aluno)
def buscar_aluno(id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, nome, matricula, curso FROM alunos WHERE id = ?", (id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrada")
    return Aluno(id=row["id"], nome=row["nome"], matricula=row["matricula"], curso=row["curso"])


#MPETODS DE EDIÇÃO!!

@app.put("/Alunos/{id}", response_model=Aluno)
def editar_aluno(id: str, dados: AlunoEntrada):
    with get_conn() as conn:
        res = conn.execute(
            "UPDATE alunos SET nome = ?, matricula = ?, curso = ? WHERE id = ?",
            (dados.nome, dados.matricula, dados.curso, id)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aluno não encontrada")
    return Aluno(id=id, **dados.model_dump())

@app.put("/Professores/{id}", response_model=Professor)
def editar_professor(id: str, dados: ProfessorEntrada):
    with get_conn() as conn:
        res = conn.execute(
            "UPDATE professores SET nome = ?, area = ? WHERE id = ?",
            (dados.nome, dados.area, id)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return Professor(id=id, ** dados.model_dump())

@app.put("/Centros/{id}", response_model= Centro)
def editar_centro(id: str, dados: CentroEntrada):
    with get_conn() as conn:
        res = conn.execute(
            "UPDATE centros SET data = ?, local = ?, vagas = ?, descricao = ? WHERE id = ? ",
            (dados.data, dados.local, dados.vagas, dados.descricao, id)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Centro não encontrado")
    return Centro(id=id, **dados.model_dump())

# MÉTODOS DE APAGAR

@app.delete("/Alunos/{id}", status_code=204)
def remover_aluno(id: str):
    with get_conn() as conn:
        res = conn.execute(
            "DELETE FROM alunos WHERE id = ?", (id,)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Aluno não encontrada")
    
@app.delete("/Professores/{id}", status_code=204)
def remover_professor(id: str):
    with get_conn() as conn:
        res = conn.execute(
            "DELETE FROM professores WHERE id = ?", (id,)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

@app.delete("/Centros/{id}", status_code=204)
def remover_centro(id: str):
    with get_conn() as conn:
        res = conn.execute(
            "DELETE FROM centros WHERE id = ?", (id,)
        )
        conn.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Centro não encontrado")