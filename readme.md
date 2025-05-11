````markdown
# 💊 Medicine Query Bot

A lightweight AI assistant that answers health‑related questions by semantically searching a local medicine dataset and responding with a small language model.

---

## 🧠 How it works

- **Embeddings** : `all‑minilm‑l6‑v2`  
  Generates dense vectors for every medicine record **and** for each user query.
- **LLM**    : `llama3.2‑1b‑instruct`  
  Crafts natural‑language answers from the retrieved data.
- **Vector store**: **FAISS** for fast similarity search.
- **Frontend**  : **Streamlit** web UI.

---

## ⚙️ Quick start

### 1 .  Install dependencies

```bash
pip install streamlit pandas requests numpy faiss-cpu
````

### 2 .  Launch the app

```bash
streamlit run app.py
```

---

## 📌 Notes

* Ensure your local embedding and LLM back‑ends (e.g. **Ollama** or **LM Studio**) are running on the ports specified in `app.py`.
* Place **`Medicine_Details.csv`** in the location expected by the code (default: project root).

---

## 🛑 Disclaimer

This project is a demo for educational purposes only and **is not a substitute for professional medical advice**. Always consult a qualified healthcare provider for personalised guidance.

```
```
