from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analysis.code_analyzer import analyze_code

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

@app.get("/")
def home():
    return {"message": "Project Doctor API running"}

@app.post("/analyze")
def analyze(input: CodeInput):
    result = analyze_code(input.code)
    return {"suggestions": result}
