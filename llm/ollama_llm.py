import subprocess
import json

def query_ollama(prompt, model="llama2"):
    command = ['ollama', 'run', model]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate(prompt.encode())
    return stdout.decode()
