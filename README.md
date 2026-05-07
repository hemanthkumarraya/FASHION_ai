# 👗 Fashion AI Studio

A full-stack fashion tech prototype featuring a customizable 3D avatar and an AI-powered fashion chatbot — built with Streamlit, Three.js, and Groq (LLaMA 3.3 70B).

---

## 🏗️ Architecture

```
app.py                          ← Streamlit entry point, layout, sidebar
components/
├── avatar_component.py         ← Three.js 3D avatar (injected HTML)
└── chatbot.py                  ← Groq LLM chatbot with session context
.streamlit/
├── config.toml                 ← Theme configuration
└── secrets.toml                ← API keys (LOCAL ONLY — gitignored)
requirements.txt
```

### Avatar Pipeline
- Three.js scene embedded via `st.components.v1.html()`
- Humanoid fashion mannequin built from parametric geometries
- Customization values injected as JS variables at render time
- Canvas API used for detailed face texture (eyes, lips, brows, blush)
- Fashion studio lighting: key light + fill + pink rim + bounce

### Chatbot Pipeline
- Groq API (`llama-3.3-70b-versatile`) for LLM inference
- Full conversation history passed with every request (context memory)
- Token-by-token streaming for real-time response display
- Domain-locked system prompt: Indian ethnic fashion expertise
- `st.session_state` for persistent chat history


## ✨ Features

### 3D Avatar
- 3 hairstyles: Elegant Bun, Long Straight, Wavy Bob
- 6 hair colors: Jet Black → Midnight Blue
- 6 skin tones: Fair Porcelain → Rich Ebony
- 8 outfit colors for saree/dress
- 6 lip colors
- Drag-to-rotate 3D interaction
- Auto-rotation with fashion studio lighting
- Screenshot/PNG export

### Fashion AI Chatbot
- Powered by LLaMA 3.3 70B via Groq
- Streaming responses (token by token)
- Full conversation context memory
- Domain: Indian ethnic wear (sarees, blouses, lehengas)
- Quick-start suggestion chips

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| App Framework | Streamlit |
| 3D Rendering | Three.js r128 |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Secrets | Streamlit Secrets Management |
| Deployment | Streamlit Community Cloud |
