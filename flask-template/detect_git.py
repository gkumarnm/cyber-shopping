import shutil
import os
import subprocess

paths = [shutil.which('git'), shutil.which('gh')]
print('which git', paths[0])
print('which gh', paths[1])
for p in paths:
    if p:
        try:
            out = subprocess.run([p, '--version'], capture_output=True, text=True)
            print(p, 'exit', out.returncode)
            print(out.stdout)
            print(out.stderr)
        except Exception as e:
            print('ERR', p, e)
