import os
import sys
import winreg

git_dir = r"C:\Program Files\Git\cmd"
if not os.path.isfile(os.path.join(git_dir, 'git.exe')):
    print('ERROR: git.exe not found in', git_dir)
    sys.exit(1)

key_path = r'Environment'
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
    try:
        current_path, _ = winreg.QueryValueEx(key, 'PATH')
    except FileNotFoundError:
        current_path = ''

paths = [p.strip() for p in current_path.split(';') if p.strip()]
normalized = [os.path.normcase(os.path.normpath(p)) for p in paths]
git_norm = os.path.normcase(os.path.normpath(git_dir))

if git_norm in normalized:
    print('Git path already present in user PATH')
else:
    if current_path and not current_path.endswith(';'):
        current_path = current_path + ';'
    new_path = current_path + git_dir
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
    print('Added Git path to user PATH:')
    print(git_dir)

print('Current user PATH entries including Git:')
user_path = os.environ.get('PATH', '')
for p in user_path.split(';'):
    if p.strip():
        print('-', p)
print('Note: Existing shells may need to be restarted for PATH changes to take effect.')
