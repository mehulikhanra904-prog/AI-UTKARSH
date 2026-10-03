# AI-UTKARSH — Academic AI Engineering Portfolio

A professional institute-inspired portfolio for **Mehuli Khanra**, B.Tech Computer Science & Engineering student. The design combines academic identity, project showcase, technical toolkit, engineering journey, and a real FastAPI + MongoDB contact backend.

## Live project

- GitHub: https://github.com/mehulikhanra904-prog/AI-UTKARSH
- Backend deployment configuration: Render via `render.yaml`

## What is included

- Professional academic/institute-style navigation
- Responsive hero with academic identity
- About, toolkit, selected work and engineering journey
- Project cards with live/demo links
- Responsive contact form
- FastAPI backend
- MongoDB Atlas persistence for contact submissions
- CORS configuration through environment variables
- Health endpoint with database connection status
- Render deployment configuration

## Tech stack

**Frontend**
- HTML5
- CSS3
- Vanilla JavaScript
- Google Fonts
- Responsive design

**Backend**
- Python
- FastAPI
- Uvicorn
- Pydantic
- Motor (MongoDB async driver)

**Database**
- MongoDB Atlas

**Deployment**
- Vercel / static hosting for frontend
- Render for FastAPI backend

## MongoDB Atlas setup

Create a MongoDB Atlas cluster and database user, then add these environment variables to your Render service:

```text
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>/<database>?retryWrites=true&w=majority
DB_NAME=ai_utkarsh
FRONTEND_URLS=https://YOUR-VERCEL-DOMAIN.vercel.app
```

For local development, copy `backend/.env.example` to your own environment configuration. **Never commit a real MongoDB password or connection string to GitHub.**

The backend automatically creates/uses the `contact_messages` collection when a contact form is submitted.

### Verify the database

Open:

`/api/health`

A working connection returns:

```json
{
  "status": "ok",
  "service": "ai-utkarsh-api",
  "database": "connected"
}
```

If the URI has not been configured, the API reports `not_configured`.

## API

- `GET /` — API status
- `GET /api/health` — backend + database health
- `GET /api/projects` — project metadata
- `POST /api/contact` — validates and stores contact messages

Contact documents contain name, email, subject, message and UTC timestamp. There is intentionally no public endpoint for reading messages.

## Local run

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend docs:

`http://127.0.0.1:8000/docs`

### Frontend

Open `index.html` with VS Code Live Server.

Before production deployment, set `window.API_BASE_URL` to the deployed FastAPI URL in the frontend configuration so the contact form targets the Render API.

## Security notes

- Database credentials are environment variables, never source code.
- Contact messages are not exposed through a public read endpoint.
- Use a strong Atlas database password.
- Configure Atlas Network Access for your deployment environment.

Built by **Mehuli Khanra** · Kolkata, India
