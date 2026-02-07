# 🚀 Deploy ke Hugging Face Spaces - Step by Step

## GitHub Repository Ready ✅
Repository: https://github.com/seritkutu-lab/hf-local-ai-space

Semua files sudah ready untuk di-deploy ke HF Spaces!

---

## 📋 STEP-BY-STEP DEPLOY KE HF SPACES

### STEP 1️⃣: Create HF Space

1. Go ke: https://huggingface.co/new-space
2. Isi form:
   - **Space name**: `local-ai` (atau nama pilihan kamu)
   - **License**: (pilih atau skip)
   - **Select the Space SDK**: Pilih **Docker** ⭐️
3. Click **Create Space**

### STEP 2️⃣: Link ke GitHub (Auto Deploy)

Ada 2 cara:

#### CARA A: Gunakan GitHub Sync (RECOMMENDED - Auto Deploy)

1. Di HF Space, pergi ke **Settings** → **Sync from GitHub**
2. Connect GitHub account (jika belum)
3. Pilih repository: `seritkutu-lab/hf-local-ai-space`
4. Pilih branch: `main`
5. Enable **Auto sync** jika mau auto-deploy setiap push ke GitHub
6. Click **Sync**

HF akan automatically pull files dari GitHub dan deploy!

#### CARA B: Manual Upload

1. Di HF Space, click **Files** → **Add file**
2. Upload tiap file:
   - `app.py`
   - `config.py`
   - `ngrok_setup.py`
   - `requirements.txt`
   - `Dockerfile`
   - `.env.example`
   - `docker-compose.yml`
   - `.gitignore`
   - `README.md`

### STEP 3️⃣: Configure Secrets

Di HF Space Settings → **Secrets**:

Tambah secret baru:
- **Key**: `NGROK_AUTH_TOKEN`
- **Value**: Token dari https://dashboard.ngrok.com/auth/your-authtoken

HF akan pass ini ke Docker container via environment variable.

### STEP 4️⃣: Set Environment (Optional)

Di **Settings** → **Docker** → **Runtime Settings**:

```
NGROK_ENABLED=True
LLM_BACKEND=ollama
OLLAMA_MODEL=mistral
```

### STEP 5️⃣: Wait untuk Build

HF akan otomatis build Docker image & deploy.

Tunggu sampai status jadi:
- 🟢 **Running** = Success!
- 🔴 **Error** = Check logs di **Logs** tab

---

## ✅ Setelah Deploy

### Access HF Space
URL akan seperti: `https://your-username-local-ai.hf.space`

Endpoints available:
- 🎨 **Web UI**: `https://your-username-local-ai.hf.space/interface`
- 📡 **API**: `https://your-username-local-ai.hf.space/api/chat`
- 📚 **Docs**: `https://your-username-local-ai.hf.space/docs`
- ✅ **Health**: `https://your-username-local-ai.hf.space/health`

---

## 🤖 Configure MetaGPT

Setelah HF Space running:

1. Get HF Space URL: `https://your-username-local-ai.hf.space`

2. Update MetaGPT config:

```yaml
llm:
  api_type: custom
  base_url: https://your-username-local-ai.hf.space
  api_endpoint: /api/chat
  model: local
  temperature: 0.7
  max_tokens: 100
```

3. Test:
```bash
curl -X POST "https://your-username-local-ai.hf.space/api/chat" \
  -H "Content-Type: application/json" \
  -d '{\"prompt\": \"Test\", \"max_tokens\": 50}'
```

---

## 🛠️ Troubleshooting HF Deployment

### Build fails
Check **Logs** tab di HF Space untuk error details.

Biasanya:
- Missing dependency → check `requirements.txt`
- Bad Dockerfile → check syntax di `Dockerfile`
- Secret not set → add NGROK_AUTH_TOKEN di Secrets

### Space says "Building..."
Normal! Bisa sampai 5-10 menit untuk first build.

### Cannot connect
- Pastikan NGROK_AUTH_TOKEN valid
- Check status di Settings → Logs
- Try refresh halaman

### API returning errors
- Check HF Space logs
- Verify NGROK_AUTH_TOKEN di env
- Test health endpoint first: `/health`

---

## 🔄 Update Code dari GitHub

Setelah setup GitHub Sync:

Untuk update space:
1. Edit files di GitHub repository
2. Push to `main` branch
3. HF Space otomatis re-deploy (jika auto-sync enabled)

Atau manual sync di HF Space:
- Settings → Sync from GitHub → Click **Sync**

---

## 📊 Monitor Space

Di HF Space Dashboard:
- **Logs**: Check application logs
- **Settings**: Change config/secrets
- **Files**: View/edit files
- **Discussion**: Enable untuk user feedback

---

## 💡 Tips

✅ **Use auto-sync**: Jangan repot deploy manual
✅ **Add secrets**: NGROK_AUTH_TOKEN HARUS ada
✅ **Monitor logs**: Check regularly untuk debug
✅ **Version numbers**: Pin exact versions di `requirements.txt`
✅ **Health checks**: Use `/health` endpoint untuk monitor

---

## 🎯 Next Steps

1. ✅ Create HF Space
2. ✅ Link ke GitHub repo
3. ✅ Add NGROK_AUTH_TOKEN secret
4. ✅ Wait untuk deployment
5. ✅ Test endpoints
6. ✅ Configure MetaGPT
7. ✅ Done! 🎉

---

## 📞 Resources

- **HF Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Docker in HF Spaces**: https://huggingface.co/docs/hub/spaces-sdks-docker
- **GitHub Integration**: https://huggingface.co/docs/hub/spaces-github
- **Secrets Management**: https://huggingface.co/docs/hub/spaces-overview#managing-secrets

---

Siap? Create HF Space sekarang di: https://huggingface.co/new-space 🚀
