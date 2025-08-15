# code_runner.py
import subprocess
import sys

def run_generated_code(code_path: str, output_path: str):
    result = subprocess.run(
        [sys.executable, code_path],  # use current Python, not system default
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\n\nErrors:\n" + result.stderr)

    return {
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }
