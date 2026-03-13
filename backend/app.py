from fastapi import FastAPI
from pydantic import BaseModel
from analysis.code_analyzer import analyze_code

app = FastAPI()

class CodeInput(BaseModel):
    code: str

@app.get("/")
def home():
    return {"message": "Project Doctor API running"}

@app.post("/analyze")
def analyze(input: CodeInput):
    result = analyze_code(input.code)
    return {"suggestions": result}
