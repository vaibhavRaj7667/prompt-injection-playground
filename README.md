# 🛡️ Prompt Injection Playground

A web app where users try to hack a secured AI agent. The agent has a **secret code** hidden in its system prompt — your mission is to extract it!

## 🎮 How It Works

A customer support AI (TechMart Bot) is protected by 5 security layers:

1. **Regex Input Guards** — blocks known injection patterns
2. **Banned Topic Filter** — blocks dangerous content
3. **Delimiter Defense** — sandboxes user input in tags
4. **PII Redaction** — removes emails, phones, cards from output
5. **Prompt Leak Detection** — blocks the agent from revealing its instructions

## 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create a .env file with: GROQ_API_KEY=your-key-here

# Run
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## 📁 Project Structure

```
├── app.py              # Streamlit UI
├── agent.py            # Secured AI agent + pipeline
├── dashboard.py        # Attack stats tracker
├── guards/
│   ├── input_guard.py  # Input validation (regex)
│   └── output_guard.py # Output filtering (PII + leaks)
├── requirements.txt
└── .gitignore
```

## 🛠️ Tech Stack

- **LLM**: LangChain + Groq
- **UI**: Streamlit
- **Language**: Python

## 📄 License

MIT
