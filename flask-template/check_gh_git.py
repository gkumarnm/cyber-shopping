import subprocess
import os

def run(cmd):
    print('CMD:', cmd)
    p = subprocess.run(cmd, capture_output=True, text=True)
    print('RET', p.returncode)
    print('OUT', p.stdout)
    print('ERR', p.stderr)

paths = [
    r'C:\Program Files\GitHub CLI\gh.exe',
    r'C:\Program Files\Git\cmd\git.exe',
]
for path in paths:
    print('CHECK PATH', path, os.path.exists(path))
    if os.path.exists(path):
        run([path, '--version'])

run([r'C:\Program Files\GitHub CLI\gh.exe', 'auth', 'status'])
