import os
os.chdir(os.path.dirname(__file__))
import app
print('app file:', app.__file__)
print('template_folder:', app.template_folder)
print('cwd:', os.getcwd())
print('db uri:', app.config['SQLALCHEMY_DATABASE_URI'])
shop_path = os.path.join(app.template_folder, 'shop.html')
print('shop path:', shop_path)
if os.path.exists(shop_path):
    with open(shop_path, 'r', encoding='utf-8') as f:
        print('shop first lines:')
        for _ in range(20):
            line = f.readline()
            if not line:
                break
            print(line.rstrip())
else:
    print('shop.html missing')
