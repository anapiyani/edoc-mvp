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

- **Backend:** [http://localhost:8000/](http://localhost:8000/api/docs/#/bitrix/bitrix_documents_create)

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

- **Frontend:** http://localhost:3000

Start the backend first so the home page can show the health check result :)
