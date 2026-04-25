from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analysis.code_analyzer import analyze_code
from analysis.github_suggester import suggest_repositories

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

class ProjectInput(BaseModel):
    project_type: str
    language: str = "python"
    page: int = 1
    per_page: int = 10

@app.get("/")
def home():
    return {"message": "Project Doctor API running"}

@app.post("/analyze")
def analyze(input: CodeInput):
    result = analyze_code(input.code)
    return {"suggestions": result}

@app.post("/suggest-repos")
def suggest_repos(input: ProjectInput):
    repos = suggest_repositories(input.project_type, input.language, input.page, input.per_page)
    return {"repositories": repos}
