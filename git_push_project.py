import os
import shutil
import subprocess
import sys

src = r"D:\myAI-Folder\Projects\WebAuth"
dst = r"D:\myAI-Folder\Projects\WebAuth\git-push"
git_exe = r"C:\Program Files\Git\cmd\git.exe"
remote_url = "https://github.com/gkumarnm/cyber-shopping.git"

if not os.path.isdir(src):
    print(f"ERROR: source path not found: {src}")
    sys.exit(1)

os.makedirs(dst, exist_ok=True)

for name in os.listdir(src):
    if name in {'.venv', 'git-push'}:
        continue
    s = os.path.join(src, name)
    d = os.path.join(dst, name)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

print('Project copy complete.')

if not os.path.isfile(git_exe):
    print(f"ERROR: git executable not found at {git_exe}")
    sys.exit(1)


def run_git(args, check=True):
    result = subprocess.run([git_exe] + args, cwd=dst, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed ({result.returncode})\n{result.stdout}\n{result.stderr}")
    return result

if not os.path.isdir(os.path.join(dst, '.git')):
    print('Initializing git repository...')
    run_git(['init', '-b', 'main'])
else:
    print('Git repository already initialized.')

remote_exists = False
try:
    remote_result = run_git(['remote', 'get-url', 'origin'], check=False)
    if remote_result.returncode == 0:
        remote_exists = True
        existing = remote_result.stdout.strip()
        print('Existing origin remote:', existing)
        if existing != remote_url:
            print('Updating origin remote URL.')
            run_git(['remote', 'set-url', 'origin', remote_url])
    else:
        print('No origin remote configured yet.')
except RuntimeError as exc:
    print('Remote check failed:', exc)

if not remote_exists:
    print('Adding origin remote.')
    run_git(['remote', 'add', 'origin', remote_url])

ignore_lines = [
    '.venv',
    '__pycache__/',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '*.log',
    '*.sqlite3',
    '*.db',
    '*.env',
    'env/',
    'venv/',
    '.Python',
    '.idea/',
    '.vscode/',
    '.DS_Store',
    'thumbs.db',
    'docker-compose.override.yml',
]
with open(os.path.join(dst, '.gitignore'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(ignore_lines) + '\n')

print('Writing .gitignore and staging files...')
run_git(['add', '.'])
try:
    run_git(['commit', '-m', 'Initial commit of cyber-shopping project'])
    print('Commit created.')
except RuntimeError as exc:
    if 'nothing to commit' in str(exc).lower():
        print('Nothing to commit; repository already up to date.')
    else:
        raise

print('Pushing to GitHub...')
push_result = run_git(['push', '-u', 'origin', 'main'])
print(push_result.stdout)
print('Push complete.')
