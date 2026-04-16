# 📄 AI Form Automation Agent

An intelligent form-filling assistant built with **Streamlit, NLP, and Playwright**.

This app allows users to:
- Fill forms using natural language (chat)
- Automatically update structured JSON data
- Visualize the form as a **real A4 document**
- Upload a **photo**
- Draw a **signature**
- Auto-fill forms in a browser using Playwright

---

## 🚀 Features

- 💬 Chat-based form filling
- 🧠 NLP-based data extraction
- 📄 Real A4 form UI (professional layout)
- 🖼️ Photo upload (top-right placement)
- ✍️ Handwritten signature support
- 🌐 Browser automation with Playwright
- 💾 JSON data persistence

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Regex / NLP
- Playwright
- Streamlit Drawable Canvas
- HTML + CSS (A4 layout)

---

## 📂 Project Structure
├── app.py
├── playwright_agent.py
├── form_data.json
├── llm_agent.py

## ⚙️ Installation

```bash
pip install streamlit playwright streamlit-drawable-canvas pillow
playwright install