import subprocess

def call_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "gemma:2b", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama error: {result.stderr.decode()}")
    return result.stdout.decode().strip()