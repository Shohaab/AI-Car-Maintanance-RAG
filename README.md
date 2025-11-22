# AI Car Maintenance RAG System

This project includes:
- FastAPI backend (RAG + Gemini)
- Streamlit UI
- In-memory vector search

## 🚀 How to run

### 1. Create virtual environment
python -m venv venv
source venv/bin/activate  (Windows: venv\Scripts\activate)

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create `.env` file
GEMINI_API_KEY=your-key-here

### 4. Run backend
uvicorn api.app:app --reload --port 8000

### 5. Run UI
streamlit run ui/app.py
