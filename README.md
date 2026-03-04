# AI Code Explainer

Transform any code snippet into a beginner-friendly, beautifully formatted explanation powered by GPT-4o-mini. Perfect for learning, teaching, and understanding complex code.

---

## 🎯 Features

✨ **AI-Powered Explanations** — Uses OpenAI's GPT-4o-mini to analyze and explain any code snippet
📚 **Beginner-Friendly** — Explanations break down code into simple steps with real-world analogies
🎨 **Beautiful UI** — Modern Streamlit frontend with dark theme and smooth interactions
⚡ **Real-Time Processing** — Instant explanations with streaming output
🔄 **Multi-Language Support** — Detects and explains code in any programming language
🚀 **Easy Setup** — Single command to launch both backend and frontend

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** — High-performance Python web framework
- **LangChain** — LLM orchestration and chain management
- **OpenAI API** — GPT-4o-mini for code analysis
- **Uvicorn** — ASGI server for running FastAPI

### Frontend
- **Streamlit** — Rapid UI development framework
- **Requests** — HTTP client for backend communication

### Configuration
- **Python-dotenv** — Secure API key management
- **Pydantic** — Data validation

---

## 📋 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone or download the project**
   ```bash
   cd AI_Code_Explainer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   Create a file at `keys/.env` and add your key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## 🚀 Usage

### Start Both Backend & Frontend

Run the single-command launcher:
```bash
python run.py
```

This will automatically start:
- **Backend API** → `http://localhost:8000`
- **Frontend UI** → `http://localhost:8501`

The frontend will open in your browser automatically.

### Manual Startup (Optional)

**Backend only:**
```bash
python -m uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend only:**
```bash
python -m streamlit run frontend/frontend.py --server.port 8501
```

---

## 📁 Project Structure

```
AI_Code_Explainer/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run.py                    # Single-command launcher
├── backend/
│   ├── __init__.py
│   └── src/
│       ├── __init__.py
│       └── main.py           # FastAPI app & LangChain chain
├── frontend/
│   └── frontend.py           # Streamlit UI
└── keys/
    └── .env                  # API credentials (not in repo)
```

---

## 🔌 API Endpoints

### POST `/explain`
Explain a code snippet.

**Request:**
```json
{
  "code": "def hello(name):\n    return f'Hello, {name}!'",
  "language": "python"
}
```

**Response:**
```json
{
  "explanation": "## 🔍 What This Code Does\n...",
  "detected_language": "python"
}
```

---

## 💡 How It Works

1. **User submits code** via the Streamlit UI
2. **Frontend sends request** to FastAPI backend
3. **Backend uses LangChain** to invoke GPT-4o-mini with a carefully crafted system prompt
4. **GPT-4o-mini analyzes** the code and generates a structured, beginner-friendly explanation
5. **Explanation is returned** and displayed beautifully in the UI

The system prompt guides the AI to:
- Explain in plain English
- Break down code step-by-step
- Use real-world analogies
- Define technical concepts
- Provide key takeaways

---

## 🔐 Security Notes

- **API Key**: Never commit `keys/.env` to version control (it's in `.gitignore`)
- **CORS**: Backend allows all origins for local development (adjust in `backend/src/main.py` for production)
- **Temperature**: Set to 0.3 for consistent, reliable explanations

---

## 📝 Example Usage

1. Paste a code snippet (any language)
2. Optionally specify the language
3. Click "Explain"
4. Get a beautifully formatted explanation with:
   - Plain English overview
   - Step-by-step breakdown
   - Real-world analogy
   - Key concepts explained
   - Takeaways to remember

---

## 🐛 Troubleshooting

**Port already in use?**
- Change port in `run.py` before launching

**OpenAI API key not found?**
- Ensure `keys/.env` exists with `OPENAI_API_KEY=your_key`
- Check file path: `keys/.env` relative to project root

**Module import errors?**
- Run `pip install -r requirements.txt` again
- Ensure Python 3.8+

---

## 📄 License

This project is provided as-is for educational and personal use.
