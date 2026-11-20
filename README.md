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
<img width="928" height="861" alt="Screenshot 2026-11-20 112618" src="https://github.com/user-attachments/assets/8c9b573b-4e79-4560-856c-5d3ca67e900c" />
<img width="437" height="417" alt="Screenshot 2026-11-20 112604" src="https://github.com/user-attachments/assets/2d72e5a0-b109-4ac1-8cf2-7b81c2712146" />
<img width="935" height="833" alt="Screenshot 2026-11-20 112522" src="https://github.com/user-attachments/assets/8d4fff43-fcb2-44fb-989f-e1b0e0390fdf" />
<img width="941" height="820" alt="Screenshot 2026-11-20 112533" src="https://github.com/user-attachments/assets/a41ba7f3-ec8b-47d0-86cb-eb08ae4da8af" />
<img width="936" height="846" alt="Screenshot 2026-11-20 112544" src="https://github.com/user-attachments/assets/7e6094f4-0771-4e07-bdfa-4d5d3b630c6b" />


