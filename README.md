# JobFit-AI
An AI-powered resume-JD matcher that scores how well a resume fits a job description, flags missing keywords, and suggests concrete improvements. Built with LangChain + GPT-4o-mini for analysis, FastAPI for the backend API, MongoDB for user/history storage, and Streamlit for the UI.


## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Notable libraries:** LangChain, FastAPI, PyMongo, python-jose (JWT), passlib (bcrypt)

## ⚡ Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/Chandangorain/JobFit-AI.git
# 2. Create & activate a virtualenv
python -m venv venv && source venv/bin/activate
# 3. Install frontend dependencies
pip install -r requirements.txt
# 4. Install backend dependencies
pip install -r backend/requirements.txt
```

## 📦 Key Dependencies
```
streamlit: latest
requests: latest
langchain: latest
langchain-openai: latest
langchain-community: latest
pypdf: latest
python-docx: latest
pydantic: latest
python-dotenv: latest
fastapi: latest
uvicorn: latest
pymongo: latest
python-jose: latest
passlib: latest
```

## 📁 Project Structure
```
.
├── app.py                    ✅ done         # Streamlit frontend (UI, auth screens)
├── requirements.txt          ✅ done         # frontend deps
└── backend/
    ├── core.py                ✅ done         # LangChain resume-JD matching pipeline
    ├── main.py                 🚧 in progress   # FastAPI app (auth + /analyze routes)
    ├── auth.py                  🚧 in progress   # password hashing + JWT
    ├── database.py               🚧 in progress   # MongoDB connection + CRUD
    └── requirements.txt        🚧 in progress   # backend deps
```

**Status legend:** ✅ done · 🚧 in progress · ⬜ not started

## 🚧 Development Phase
| Component | File | Status | Notes |
|---|---|---|---|
| Resume/JD matching logic | `backend/core.py` | ✅ Done | LangChain chain + structured output via Pydantic |
| Streamlit UI | `app.py` | ✅ Done | Sign in/up UI, JD + resume input, results display |
| Auth API | `backend/main.py`, `backend/auth.py` | 🚧 In progress | JWT-based signup/login, needs testing end-to-end |
| Database layer | `backend/database.py` | 🚧 In progress | MongoDB user + analysis history storage |
| Deployment config | — | ⬜ Not started | Dockerfile / hosting setup pending |

## 🛠️ Development Setup
### Python
1. Install Python (v3.10+ recommended)
2. `python -m venv venv && source venv/bin/activate`  (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt` and `pip install -r backend/requirements.txt`

### Running locally
```bash
# Terminal 1: MongoDB (if not already running)
docker run -d -p 27017:27017 --name jobfit-mongo mongo:latest

# Terminal 2: backend
cd backend
export OPENAI_API_KEY="sk-..."
uvicorn main:app --reload --port 8000

# Terminal 3: frontend
streamlit run app.py
```



Please follow the existing code style and include tests for new behavior where applicable.

---

<div align="center">

[![Made with ReadmeBuddy](https://img.shields.io/badge/Made%20with-ReadmeBuddy-8B5CFF?style=for-the-badge&logo=markdown&logoColor=white)](https://readmebuddy.com)

<sub>Generate beautiful READMEs in seconds → <a href="https://readmebuddy.com">readmebuddy.com</a></sub>

</div>
