import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Load API key from keys/.env ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", "..", "keys", ".env")
load_dotenv(dotenv_path=ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found. Check keys/.env")

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Code Explainer API",
    description="Explains any code snippet using GPT-4o-mini via LangChain",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response Schemas ────────────────────────────────────────────────
class CodeRequest(BaseModel):
    code: str
    language: str = "auto-detect"

class ExplainResponse(BaseModel):
    explanation: str
    detected_language: str

# ── LangChain Chain ───────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY,
)

SYSTEM_PROMPT = """You are an expert code explainer who makes programming accessible to everyone — \
both technical developers and complete beginners.

When given a code snippet, produce a rich, friendly, and well-structured explanation in Markdown \
using the exact sections below. Always use emojis for section headings and keep language simple. \
When you must use a technical term, briefly explain it in plain English right after in parentheses.

---

## 🔍 What This Code Does
Write 2-3 sentences in plain English that anyone — even your grandmother — can understand. \
Focus on the PURPOSE, not the mechanics.

## 🏷️ Language & Technologies
- **Language detected:** (name the programming language)
- **Key libraries / frameworks used:** (list them, or write "None" if not applicable)

## 📋 Step-by-Step Breakdown
Walk through each logical block of the code one by one. Use numbered steps. \
For each step write:
- What the code says (in plain English, not code)
- Why it matters

## 💡 Real-World Analogy
Create a vivid, relatable real-world analogy (like a recipe, a shop, a post office, etc.) \
that mirrors exactly what this code does. Zero technical jargon here.

## ⚙️ Key Concepts Used
List every important programming concept that appears (e.g., loops, functions, APIs, classes). \
For each concept give exactly ONE plain-English sentence explaining it as if talking to a 10-year-old.

## ✅ Key Takeaways
Provide 4-5 bullet points summarising the most important things a reader should remember \
after reading this code.

---
Format everything in clean Markdown so it renders beautifully."""

HUMAN_PROMPT = """Language hint: {language}

Code to explain:
```
{code}
```"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT),
])

chain = prompt | llm | StrOutputParser()

# ── Helper: detect language from explanation ──────────────────────────────────
def _extract_language(explanation: str, hint: str) -> str:
    """Pull the detected language from the response or fall back to the hint."""
    for line in explanation.splitlines():
        if "Language detected" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                lang = parts[1].strip().strip("*").strip()
                if lang:
                    return lang
    return hint if hint != "auto-detect" else "Unknown"

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "AI Code Explainer API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/explain", response_model=ExplainResponse)
async def explain_code(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    try:
        explanation = chain.invoke({
            "language": request.language,
            "code": request.code,
        })
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(exc)}")

    detected = _extract_language(explanation, request.language)
    return ExplainResponse(explanation=explanation, detected_language=detected)
