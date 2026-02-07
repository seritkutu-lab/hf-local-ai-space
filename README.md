# 🤖 Local AI HF Space dengan ngrok Tunnel

Aplikasi Hugging Face Space untuk menjalankan AI model lokal dengan akses remote via ngrok tunnel. Cocok untuk integrasi dengan MetaGPT dan aplikasi lainnya.

## ✨ Fitur

- ✅ **FastAPI Backend** - REST API untuk queries
- ✅ **Gradio Interface** - Web UI yang user-friendly  
- ✅ **ngrok Tunnel** - Public URL untuk remote access
- ✅ **MetaGPT Ready** - Compatible configuration untuk MetaGPT
- ✅ **Multiple LLM Backends** - Support Ollama, GPT4All, HuggingFace, LlamaCpp
- ✅ **Easy Configuration** - Via .env file
- ✅ **Docker Ready** - Bisa di-deploy ke HF Spaces

## 🚀 Quick Deploy ke HF Spaces

### 1. Create HF Space
- Go to https://huggingface.co/new-space
- Choose: **Space SDK** = `Docker`
- Name: `local-ai` (atau nama lain)
- Click **Create Space**

### 2. Clone Repository
```bash
git clone https://huggingface.co/spaces/your-username/local-ai
cd local-ai
```

### 3. Copy Files
Copy semua file dari repo ini ke HF Space folder:
- app.py
- config.py
- ngrok_setup.py
- requirements.txt
- Dockerfile
- .env.example
- docker-compose.yml
- .gitignore
- README.md

### 4. Configure
```bash
cp .env.example .env
# Edit .env dan isi NGROK_AUTH_TOKEN
```

### 5. Push ke HF Spaces
```bash
git add .
git commit -m "Setup local AI space"
git push origin main
```

HF akan otomatis build dan deploy!

---

## 📡 API Endpoints

| Endpoint | Method | Deskripsi |
|----------|--------|----------|
| `/` | GET | Server status |
| `/health` | GET | Health check |
| `/api/chat` | POST | Main chat API |
| `/interface` | GET | Gradio web UI |
| `/docs` | GET | API documentation |

---

## 🤖 MetaGPT Integration

Setelah HF Space running, configure MetaGPT:

```yaml
llm:
  api_type: custom
  base_url: https://your-space.hf.space
  api_endpoint: /api/chat
  model: local
  temperature: 0.7
```

CURL test:
```bash
curl -X POST "https://your-space.hf.space/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "max_tokens": 100}'
```

---

## 📚 Supported LLM Models

### Ollama (Recommended)
```bash
ollama run mistral          # 7B - fast & good
ollama run llama2           # 7B/13B/70B
ollama run neural-chat      # 7B
ollama run dolphin-mixtral  # 46.7B MoE
```

### HuggingFace
```env
HF_MODEL_ID=gpt2
HF_DEVICE=cpu
```

---

## 📄 License

MIT License

---

Starred? Consider supporting! 🌟
