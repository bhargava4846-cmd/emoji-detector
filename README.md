# 🤖 AI Emoji Detector

An AI-powered web application that analyzes the emotion behind any text and suggests the most fitting emojis — built with Python, Flask, Claude AI, LangChain, ChromaDB (RAG), and a vanilla HTML/CSS/JS frontend.

---

## 🌟 Live Demo

> Run locally — see setup instructions below.

---

## 📸 What It Does

Type any sentence and the AI will:
- Understand the **emotion and context** behind your words
- Search a **vector database** of emojis for the closest matches
- Ask **Claude AI** to pick the best 3–5 emojis with an explanation
- Display each emoji with its **name label** and a copyable result

**Example:**

| Input | Output |
|---|---|
| `I just got promoted at work!` | 🎉 Party Popper · 🏆 Trophy · 🥳 Partying Face · 😄 Grinning Face |
| `Feeling sad and lonely today` | 😢 Crying Face · 💔 Broken Heart · 😞 Disappointed Face |
| `Going to the gym, let's go!` | 💪 Flexed Biceps · 🔥 Fire · 🚀 Rocket |

---

## ✨ Features

- **AI Emoji Detection** — Claude analyzes sentiment and picks the best emojis
- **RAG Pipeline** — Retrieval-Augmented Generation using ChromaDB vector search
- **Safe Search Toggle** — Family-friendly mode ON by default; adult content requires age confirmation
- **Emoji Name Labels** — Every result shows the emoji + its official name
- **Copy to Clipboard** — One click copies just the emoji characters
- **Example Prompts** — 6 quick-fill chips to try instantly
- **Keyboard Shortcut** — `Ctrl + Enter` to submit
- **Character Counter** — Live count as you type

---

## 🧠 How It Works (Architecture)

```
Browser (index.html)
       │
       │  POST /detect  { text, safe_search }
       ▼
Flask Web Server (app.py) — port 5000
       │
       ▼
LangChain Pipeline (emoji_chain.py)
       │
       ├──► ChromaDB Vector Database (vector_store.py)
       │         Converts text → vector
       │         Finds 10 closest emoji vectors
       │         Filters by safe_search setting
       │         Returns candidate emojis
       │
       └──► Claude API (claude-sonnet-4-6)
                 Reads candidates + user text
                 Picks best 3–5 emojis
                 Returns JSON with explanation
       │
       ▼
Response: [{ emoji, name }] + explanation
       │
       ▼
Browser renders emoji cards with names
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML, CSS, JavaScript | User interface |
| **Backend** | Python 3.14, Flask | Web server & API |
| **AI Model** | Claude Sonnet 4.6 (Anthropic) | Emoji selection & reasoning |
| **AI Framework** | LangChain | LLM orchestration |
| **Vector Database** | ChromaDB | Emoji similarity search (RAG) |
| **Secret Management** | python-dotenv | Secure API key loading |
| **Version Control** | Git + GitHub | Source control |

---

## 📁 Project Structure

```
emoji-detector/
│
├── backend/
│   ├── app.py              # Flask web server — routes & HTTP handling
│   ├── emoji_chain.py      # LangChain + Claude AI pipeline (RAG)
│   ├── vector_store.py     # ChromaDB setup & vector search
│   ├── emoji_data.py       # Emoji knowledge base (41 emojis)
│   └── requirements.txt    # Python package list
│
├── frontend/
│   ├── index.html          # Main web page
│   ├── style.css           # Styling & dark theme
│   └── app.js              # Browser logic & API calls
│
├── .env                    # Secret keys — NOT committed to Git
├── .gitignore              # Excludes .env, venv/, .chroma/
└── README.md               # This file
```

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.10+](https://python.org/downloads) — check "Add Python to PATH" during install
- [Git](https://git-scm.com/download/win)
- [VS Code](https://code.visualstudio.com) (recommended)
- An [Anthropic API key](https://console.anthropic.com) with credits

---

### 1. Clone the Repository

```bash
git clone https://github.com/bhargava4846-cmd/emoji-detector.git
cd emoji-detector
```

---

### 2. Create a Virtual Environment

```bash
# Create the private Python toolbox
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### 4. Add Your API Key

Create a `.env` file in the root folder:

```
ANTHROPIC_API_KEY=your-api-key-here
```

> Get your key from [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key

---

### 5. Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

---

### 6. Open the Frontend

Open `frontend/index.html` in your browser:
- **VS Code:** Right-click the file → Open with Live Server
- **Direct:** Double-click `frontend/index.html` in Windows Explorer

---

## 🔌 API Reference

### `GET /`
Health check — confirms the server is running.

**Response:**
```json
{ "status": "Emoji Detector API is running!" }
```

---

### `POST /detect`
Analyzes text and returns matching emojis.

**Request Body:**
```json
{
  "text": "I just got promoted at work!",
  "safe_search": true
}
```

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | Yes | — | The text to analyze |
| `safe_search` | boolean | No | `true` | `false` allows adult emoji results |

**Response:**
```json
{
  "emojis": [
    { "emoji": "🎉", "name": "Party Popper" },
    { "emoji": "🏆", "name": "Trophy" },
    { "emoji": "🥳", "name": "Partying Face" }
  ],
  "explanation": "These emojis capture the celebratory excitement of a well-earned promotion."
}
```

---

## 🧩 Key Concepts Used

### RAG (Retrieval-Augmented Generation)
Instead of asking Claude to freely generate emojis (which could hallucinate), we first retrieve the most relevant emojis from ChromaDB, then give Claude only those candidates to choose from. This grounds the AI in real data.

### Vector Search
Each emoji's description is converted into a list of numbers (a vector) that represents its meaning. When you search, your text is also converted to a vector and ChromaDB finds the emojis whose vectors are mathematically closest — meaning most similar in meaning.

### LLM Temperature
Set to `0.7` — a balance between predictable (0.0) and creative (1.0). This gives varied, interesting suggestions without going off-topic.

### Safe Search
Emojis are tagged `"safe"` or `"adult"` in the knowledge base. When safe search is ON, adult emojis are filtered out before Claude even sees the candidates. Turning it off requires the user to confirm they are 18+.

---

## 🔧 Adding New Emojis

1. Open `backend/emoji_data.py`
2. Add a new entry to `EMOJI_DATA`:

```python
{
    "emoji": "🦋",
    "name": "butterfly",
    "emotions": "transformation, beauty, freedom, change",
    "tags": "change growth freedom beautiful nature transformation",
    "content_rating": "safe"
}
```

3. Delete the `.chroma/` folder (forces database rebuild)
4. Restart the server — it will reload all emojis automatically

---

## 🛡️ Security Notes

- **API key** is stored in `.env` and excluded from Git via `.gitignore` — never hardcoded
- **Safe search** is ON by default — adult content requires explicit opt-in with age confirmation
- **Input validation** rejects empty or malformed requests before they reach the AI
- **CORS** is enabled for local development — restrict origins before deploying to production

---

## 🗺️ Roadmap / Future Ideas

- [ ] Deploy backend to Render or Railway (make it accessible online)
- [ ] Deploy frontend to Vercel or Netlify
- [ ] Add search history saved to a local database
- [ ] Support multiple languages
- [ ] Add emotion category label (happy / sad / angry) alongside emojis
- [ ] Increase emoji database from 41 to 200+

---

## 📚 What I Learned Building This

| Concept | Where Used |
|---|---|
| Python Flask web server | `app.py` |
| REST API design (GET/POST) | `/` and `/detect` endpoints |
| Claude API via Anthropic | `emoji_chain.py` |
| LangChain LLM orchestration | `emoji_chain.py` |
| Vector embeddings & similarity | `vector_store.py` |
| ChromaDB (Vector Database) | `vector_store.py` |
| RAG pattern | `emoji_chain.py` + `vector_store.py` |
| LLM temperature tuning | `ChatAnthropic(temperature=0.7)` |
| HTML / CSS / JavaScript | `frontend/` folder |
| Async/await & Fetch API | `app.js` |
| Safe search / content filtering | Toggle UI + backend filter |
| Git version control + GitHub | Throughout the project |
| Python virtual environments | `venv/` |
| Secret key management | `.env` + `python-dotenv` |

---

## 👤 Author

**Abhi Bhargava**
- GitHub: [@bhargava4846-cmd](https://github.com/bhargava4846-cmd)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with Claude AI · LangChain · ChromaDB · Flask*
