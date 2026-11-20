# Email Reply Assistant (LLM Mini Project - PS 6)

**Problem statement:** Writing professional email replies takes effort. This app takes a pasted email and returns three reply drafts: formal, friendly and short.

**Stack:** Python, Streamlit, Groq API (openai/gpt-oss-20b with fallbacks)

## Features
- Three reply styles in tabs, with word count and a copy button
- Sample emails to try quickly
- Optional instruction and sign-off name
- Download all replies as a .txt file

## How to run
```
pip install -r requirements.txt
copy .env.example .env      # then put your own GROQ_API_KEY in .env
streamlit run app.py
```

Test inputs are in `sample_emails.txt`.

## Screenshots
(Add 1-2 screenshots here)
