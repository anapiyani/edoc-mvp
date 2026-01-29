## Run backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

- **Backend:** http://localhost:8000
- **Swagger:** http://localhost:8000/api/docs/

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

- **Frontend:** http://localhost:3000

## 1) Upload PDF (Bitrix imitation)

```bash
curl -X POST http://localhost:8000/api/bitrix/documents/ \
  -F "deal_id=123" \
  -F "doc_id=DOC-001" \
  -F "file=@test.pdf"
```

Expected response:

- JSON with `sign_url` (e.g. `http://localhost:3000/sign/<token>`) and `status=awaiting_decision`.

## 2) Client page

Open the returned `sign_url` in the browser:

- PDF is displayed
- PDF can be downloaded
- Accept / Reject buttons are available

## Notes

- Files are stored locally in `backend/media/`.
- Default DB: SQLite (`backend/db.sqlite3`).
