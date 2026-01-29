## Run backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 8000
```

- **Backend:** http://localhost:8000
- **Health:** http://localhost:8000/api/health/

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

- **Frontend:** http://localhost:3000
- **Home:** http://localhost:3000/
- **Sign placeholder:** http://localhost:3000/sign/testtoken

Start the backend first so the home page can show the health check result. CORS and proxy are set so the frontend can call the backend without CORS issues.
