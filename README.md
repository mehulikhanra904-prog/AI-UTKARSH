# AI-UTKARSH — Academic AI Engineering Portfolio

A professional institute-inspired portfolio for **Mehuli Khanra**, B.Tech Computer Science & Engineering student. The site combines academic identity, project showcase, technical toolkit, engineering journey, and a FastAPI + MongoDB contact backend.

## Configuration

Deployment-specific values are intentionally kept out of application source code.

### Vercel frontend

Add this environment variable to the Vercel project:

```text
API_BASE_URL=<your-deployed-fastapi-base-url>
```

Vercel generates `api-config.js` during the build from this variable. The API URL is therefore not stored in `index.html` or `script.js`.

### Render backend

Add these environment variables to the Render service:

```text
MONGODB_URI=<your-mongodb-connection-string>
DB_NAME=<your-database-name>
FRONTEND_URLS=<your-vercel-origin>
```

The backend requires all three values and does not use localhost, database-name, or CORS fallbacks.

For local development, use your own environment configuration. Never commit real credentials or deployment URLs that are intended to remain configurable.

## What is included

- Professional academic/institute-style navigation
- Responsive hero with academic identity
- About, toolkit, selected work and engineering journey
- Project cards with live/demo links
- Responsive contact form
- FastAPI backend
- MongoDB Atlas persistence for contact submissions
- Environment-driven CORS and database configuration
- Environment-driven frontend API configuration
- Health endpoint with database connection status
- Vercel and Render deployment configuration

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

Set the required backend environment variables before starting the API.

Backend docs are available at the configured local API origin followed by `/docs`.

### Frontend

Set `API_BASE_URL` in your local environment/build configuration, then open `index.html` with your static development server.

## Security notes

- Database credentials are environment variables, never source code.
- Deployment-specific API origins are environment variables, never source code.
- Contact messages are not exposed through a public read endpoint.
- Use a strong Atlas database password.
- Configure Atlas Network Access for your deployment environment.

Built by **Mehuli Khanra**.
