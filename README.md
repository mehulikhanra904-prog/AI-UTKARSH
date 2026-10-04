# 🚀 AI UTKARSH — Academic & Career Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/AI-UTKARSH-7C3AED?style=for-the-badge&logo=ai&logoColor=white" />
  <img src="https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Live-22C55E?style=for-the-badge" />
</p>

<p align="center">
  <b>Learn with direction. Grow with intent. Build for the future.</b>
</p>

<p align="center">
  AI-assisted academic, skill development, project showcase and career-readiness platform built for students.
</p>

---

## 🌐 Live Demo

### ⭐ AI UTKARSH — Live Frontend

👉 **https://ai-utkarsh-frontend-ex54.vercel.app/**

### 💻 GitHub Repository

👉 **https://github.com/mehulikhanra904-prog/AI-UTKARSH**

---

# 📌 About AI UTKARSH

**AI UTKARSH** is an AI-assisted student workspace designed to bring academics, technical skills, projects and career preparation into one structured platform.

Instead of keeping college learning, coding practice, projects and placement preparation separate, AI UTKARSH provides a unified command center for a student's engineering journey.

### 🎯 Core idea

```
Learn → Practice → Build → Deploy → Measure → Improve → Prepare
```

The platform is designed to help students move from **learning concepts** to **building real-world evidence of their skills**.

---

# ✨ Key Features

## 📚 Academic Command Center

Organize academic learning around important Computer Science foundations such as:

- Data Structures & Algorithms
- Database Management Systems
- Operating Systems
- Computer Architecture
- Software Engineering
- Artificial Intelligence

The goal is to connect academic concepts with practical engineering skills.

---

## 🧠 Skill Intelligence

Track technical development across areas such as:

- Python
- C / C++
- JavaScript
- React
- Backend Development
- FastAPI
- Machine Learning
- Generative AI
- DSA
- Databases
- Cloud & Deployment
- Git & GitHub

The platform encourages identifying skill gaps and converting them into actionable learning priorities.

---

## 💻 Project Portfolio

Projects are treated as practical evidence of learning.

The platform showcases projects across:

- Artificial Intelligence
- Machine Learning
- Generative AI
- Full-Stack Development
- Backend Engineering
- Computer Vision
- Security
- Student Productivity

Each project can be connected to its technology stack, purpose and live deployment.

---

## 🎯 Career Readiness

AI UTKARSH connects technical development with career preparation.

Focus areas include:

- DSA preparation
- Backend development
- AI / ML
- Generative AI
- GitHub
- Open Source
- Projects
- Deployment
- Internship preparation
- Placement preparation
- Interview readiness

---

## 🗺️ Engineering Roadmap

The platform follows a progressive learning model:

```
FOUNDATION
   ↓
PROGRAMMING + DSA
   ↓
FULL-STACK DEVELOPMENT
   ↓
MACHINE LEARNING
   ↓
GENERATIVE AI
   ↓
AI AGENTS
   ↓
PRODUCTION AI SYSTEMS
   ↓
INTERNSHIPS + CAREER
```

---

# 🏗️ Architecture

```
                    ┌─────────────────────┐
                    │       Student       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Frontend         │
                    │ HTML / CSS / JS     │
                    │ Responsive UI       │
                    └──────────┬──────────┘
                               │
                         REST API Calls
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    │                     │
                    │ Projects            │
                    │ Contact             │
                    │ Health              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    MongoDB Atlas    │
                    │                     │
                    │ Contact Messages    │
                    │ Application Data    │
                    └─────────────────────┘
```

---

# 🛠️ Tech Stack

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Google Fonts
- Responsive design
- Vercel

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Motor

## Database

- MongoDB
- MongoDB Atlas

## Development & Deployment

- Git
- GitHub
- VS Code
- PowerShell
- Vercel
- Render

---

# 📂 Project Structure

```
AI-UTKARSH/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── README.md
└── .gitignore
```

> The exact structure can change as new features are added.

---

# 🔌 API

The backend exposes REST endpoints for the application.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/api/health` | Backend and database health |
| GET | `/api/projects` | Project metadata |
| POST | `/api/contact` | Validate and store contact messages |

### API Documentation

When running locally:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger API documentation.

---

# ⚙️ Configuration

Deployment-specific values are kept outside the source code.

## Frontend

Configure:

```text
API_BASE_URL=<your-deployed-fastapi-base-url>
```

The frontend can use this value to communicate with the deployed backend.

## Backend

Configure:

```text
MONGODB_URI=<your-mongodb-connection-string>
DB_NAME=<your-database-name>
FRONTEND_URLS=<your-vercel-origin>
```

Never commit real credentials, API keys or database passwords.

---

# 💻 Local Development

## 1. Clone the Repository

```powershell
git clone https://github.com/mehulikhanra904-prog/AI-UTKARSH.git
cd AI-UTKARSH
```

---

## 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Set the required environment variables and run:

```powershell
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Setup

Configure the frontend API base URL for your local backend and start the static frontend using your preferred development server.

The deployed application is available at:

👉 **https://ai-utkarsh-frontend-ex54.vercel.app/**

---

# 🚀 Deployment

## Frontend — Vercel

The production frontend is deployed on Vercel.

### Live:

👉 **https://ai-utkarsh-frontend-ex54.vercel.app/**

---

## Backend — Render

The FastAPI backend can be deployed independently on Render.

Production architecture:

```
Vercel Frontend
      │
      │ HTTPS
      ▼
Render FastAPI Backend
      │
      ▼
MongoDB Atlas
```

---

# 🔐 Security

Important security practices:

- Never commit `.env` files containing secrets.
- Never expose MongoDB credentials in frontend code.
- Keep deployment URLs configurable where appropriate.
- Use a strong MongoDB password.
- Configure MongoDB Atlas Network Access correctly.
- Do not expose private contact submissions through a public GET endpoint.

Example files that should remain private:

```
.env
.env.local
.env.production
credentials.json
secrets.json
```

---

# 📊 Development Philosophy

AI UTKARSH follows a practical engineering loop:

### 01 — Learn

Build strong fundamentals.

### 02 — Practice

Solve problems and experiment.

### 03 — Build

Create real-world projects.

### 04 — Deploy

Make projects accessible online.

### 05 — Document

Maintain professional GitHub repositories and documentation.

### 06 — Improve

Measure progress and continuously close skill gaps.

---

# 🗺️ Future Roadmap

## Phase 1 — Foundation

- [x] Academic portfolio
- [x] Skills / toolkit section
- [x] Project showcase
- [x] Engineering journey
- [x] Contact system
- [x] FastAPI backend
- [x] MongoDB persistence
- [x] Vercel deployment
- [x] Render-ready backend

## Phase 2 — Intelligence

- [ ] AI skill-gap analysis
- [ ] Personalized learning recommendations
- [ ] Career readiness score
- [ ] Personalized roadmap generation
- [ ] Resume analysis
- [ ] Internship recommendations

## Phase 3 — Student Intelligence

- [ ] DSA progress tracking
- [ ] GitHub activity analysis
- [ ] Project quality evaluation
- [ ] Placement preparation tracker
- [ ] Interview preparation

## Phase 4 — Advanced AI

- [ ] RAG-based academic assistant
- [ ] AI career mentor
- [ ] AI interview simulator
- [ ] AI project evaluator
- [ ] Agentic learning workflows
- [ ] Personalized AI learning agent

---

# 🤝 Contributing

Contributions, suggestions and improvements are welcome.

### Create a feature branch

```bash
git checkout -b feature/your-feature
```

### Make changes

```bash
git add .
git commit -m "feat: add your feature"
```

### Push

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 🐛 Issues & Suggestions

If you discover a bug or have a feature idea:

1. Open a GitHub issue.
2. Clearly describe the problem or idea.
3. Add reproduction steps for bugs.
4. Explain the expected behavior.
5. Submit the issue for discussion.

---

# 👩‍💻 Developer

## Mehuli Khanra

**B.Tech Computer Science & Engineering**

### Areas of Interest

- 🤖 Artificial Intelligence
- 🧠 Machine Learning
- ✨ Generative AI
- 🕸️ Full-Stack Development
- ⚙️ Backend Engineering
- 🧩 Data Structures & Algorithms
- 🌐 Web3
- 🚀 Open Source

### GitHub

👉 https://github.com/mehulikhanra904-prog

---

# 🌐 Live Project

## ⭐ AI UTKARSH

**Academic Intelligence • Skill Development • Projects • Career Readiness**

👉 **https://ai-utkarsh-frontend-ex54.vercel.app/**

---

# ⭐ Support the Project

If you find AI UTKARSH useful or interesting:

⭐ Star the repository

🍴 Fork the project

🐛 Report bugs

💡 Suggest features

🤝 Contribute

---

# 💜 Final Vision

AI UTKARSH is designed to become more than a portfolio.

It is a structured system for turning a student's learning journey into measurable engineering progress.

```
              📚 LEARN
                 ↓
          🧠 BUILD SKILLS
                 ↓
          💻 BUILD PROJECTS
                 ↓
             🚀 DEPLOY
                 ↓
            📊 MEASURE
                 ↓
            🎯 PREPARE
                 ↓
        🤖 BUILD AI SYSTEMS
                 ↓
          🚀 ENGINEER CAREER
```

> **Learn with direction. Grow with intent. Build in public.**

---

<p align="center">
  <b>🚀 AI UTKARSH</b><br/>
  Academic Intelligence • Skill Development • Projects • Career Readiness
</p>

<p align="center">
  Built with curiosity, consistency and code by <b>Mehuli Khanra</b>.
</p>
