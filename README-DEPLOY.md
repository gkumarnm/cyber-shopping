## Running locally (venv)

Activate the existing venv and run the app:

```powershell
Set-Location D:\myAI-Folder\Projects\WebAuth\flask-template
.\..\.venv\Scripts\Activate.ps1
python app.py
```

## Docker

Build and run the container:

```bash
docker build -t flask-auth-app .
docker run -p 5000:5000 flask-auth-app
```

Or with docker-compose:

```bash
docker-compose up --build
```
