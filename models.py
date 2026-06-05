from pydantic import BaseModel

class AlunoEntrada(BaseModel):
    nome: str
    matricula: str
    curso: str

class Aluno(AlunoEntrada):
    id: str

class ProfessorEntrada(BaseModel):
    nome: str
    area: str

class Professor(ProfessorEntrada):
    id: str

class CentroEntrada(BaseModel):
    data: str
    local: str
    vagas: int
    descricao: str

class Centro(CentroEntrada):
    id: str