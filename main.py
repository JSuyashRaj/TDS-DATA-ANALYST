from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import os

from .llm_client import generate_code_from_llm
from .code_runner import run_generated_code

app = FastAPI(title="Simple Data Analyst Agent", version="1.2")

QUESTION_FILE = "question.txt"
OUTPUT_FILE = "output.txt"
GENERATED_CODE_FILE = "generated_code.py"


@app.get("/")
def read_root():
    return {"message": "Data Analyst API is running. Go to /docs to test."}


def process_question(question: str):
    # Save question for record
    with open(QUESTION_FILE, "w", encoding="utf-8") as f:
        f.write(question)

    # Get code from LLM
    generated_code = generate_code_from_llm(question)
    with open(GENERATED_CODE_FILE, "w", encoding="utf-8") as f:
        f.write(generated_code)

    # Run the code
    run_result = run_generated_code(GENERATED_CODE_FILE, OUTPUT_FILE)

    return {
        "question": question,
        "output_file": OUTPUT_FILE,
        "stdout": run_result["stdout"],
        "stderr": run_result["stderr"],
        "returncode": run_result["returncode"]
    }

@app.get("/run")
async def run_from_file():
    if not os.path.exists(QUESTION_FILE):
        return JSONResponse({"error": f"{QUESTION_FILE} not found"}, status_code=400)

    with open(QUESTION_FILE, "r", encoding="utf-8") as f:
        question = f.read().strip()

    if not question:
        return JSONResponse({"error": "Question file is empty"}, status_code=400)

    return JSONResponse(process_question(question))

@app.post("/run")
async def run_from_body(question: str = Body(None, description="Your question for the Data Analyst Agent")):
    if not question:
        if os.path.exists(QUESTION_FILE):
            with open(QUESTION_FILE, "r", encoding="utf-8") as f:
                question = f.read().strip()
        else:
            return JSONResponse({"error": "No question provided and no question.txt found"}, status_code=400)

    if not question:
        return JSONResponse({"error": "Question is empty"}, status_code=400)

    return JSONResponse(process_question(question))
