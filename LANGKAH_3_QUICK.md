# ⚡ LANGKAH 3 QUICK - Copy Paste Commands

Ikuti step ini untuk fastest setup. Copy-paste langsung di PowerShell!

---

## 🎯 QUICK PATH (5-10 menit)

### ✅ STEP 1: Prepare

```powershell
# Setup folder
cd $HOME
mkdir hf-spaces
cd hf-spaces
```

### ✅ STEP 2: Clone HF Space

```powershell
# CHANGE: hasyiem → your HF username, local-ai → your space name
git clone https://huggingface.co/spaces/hasyiem/local-ai
cd local-ai
```

### ✅ STEP 3: Get Files from GitHub

**OPTION A - Recommended (Copy-Paste)**

```powershell
# Method: Add GitHub as remote & pull
git remote add github https://github.com/seritkutu-lab/hf-local-ai-space.git
git pull github main --allow-unrelated-histories

# Jika ada conflict di README, resolve dengan:
# git checkout --ours README.md
# git add README.md && git commit
```

**OPTION B - Simpler (Manual Download)**

```powershell
# 1. Download ZIP: https://github.com/seritkutu-lab/hf-local-ai-space/archive/refs/heads/main.zip
# 2. Extract & copy files to local-ai folder
# 3. Continue ke STEP 4
```

### ✅ STEP 4: Configure .env

```powershell
# Copy template
copy .env.example .env

# Edit dengan text editor
notepad .env

# Find & change:
# NGROK_AUTH_TOKEN=your_actual_token_here
# (Get token dari: https://dashboard.ngrok.com/auth/your-authtoken)
```

### ✅ STEP 5: Commit & Push ke HF

```powershell
git add .
git commit -m "Setup local AI space with ngrok - $(Get-Date -Format 'yyyy-MM-dd')"
git push origin main
```

### ✅ STEP 6: Monitor Build

Buka di browser:
```
https://huggingface.co/spaces/[your-username]/local-ai/settings
```

Lihat tab **"Logs"** - tunggu sampai status = 🟢 **Running**

---

## 🔐 STEP 7: Add Secret (CRITICAL!)

Buka HF Space Settings:

1. Go: `https://huggingface.co/spaces/[your-username]/local-ai/settings`
2. Scroll ke **"Secrets"** section
3. Click **"Add Secret"**
4. Fill:
   ```
   Name: NGROK_AUTH_TOKEN
   Value: [your token from https://dashboard.ngrok.com]
   ```
5. Click **"Add"**
6. Space akan auto-restart

---

## ✅ STEP 8: Verify Deploy Success

Setelah 🟢 Running status:

### Test via Browser

Open these URLs (replace `[username]` with your HF username):

1. **Health Check**: 
   ```
   https://[username]-local-ai.hf.space/health
   ```
   Expected: `{"status":"healthy","service":"running"}`

2. **Web UI**:
   ```
   https://[username]-local-ai.hf.space/interface
   ```
   Should show Gradio chat interface

3. **API Docs**:
   ```
   https://[username]-local-ai.hf.space/docs
   ```
   Should show Swagger API documentation

### Test via PowerShell

```powershell
# Health check
curl https://[username]-local-ai.hf.space/health

# Test API
curl -X POST "https://[username]-local-ai.hf.space/api/chat" `
  -H "Content-Type: application/json" `
  -d '{\"prompt\": \"Hello world\", \"max_tokens\": 50}'
```

---

## 🤖 STEP 9: Configure MetaGPT

Update your MetaGPT `config.yaml`:

```yaml
llm:
  api_type: custom
  base_url: https://[username]-local-ai.hf.space
  api_endpoint: /api/chat
  model: local
  temperature: 0.7
  max_tokens: 100
```

Or environment variables:
```powershell
$env:METAGPT_LLM_API_BASE="https://[username]-local-ai.hf.space"
$env:METAGPT_LLM_MODEL="local"
```

---

## 🆘 If Something Goes Wrong

### Issue: Build still ERROR saat sudah 10+ menit

**Check**:
1. Open `https://huggingface.co/spaces/[username]/local-ai/settings` → **Logs**
2. Scroll ke error message

**Most common**: 
```
NGROK_AUTH_TOKEN: not set or invalid
```

**Fix**: Add secret di HF Space (STEP 7 atas)

### Issue: "fatal: not a git repository"

```powershell
# Re-clone HF Space
cd $HOME/hf-spaces
rm -r local-ai
git clone https://huggingface.co/spaces/[username]/local-ai
cd local-ai
git remote add github https://github.com/seritkutu-lab/hf-local-ai-space.git
git pull github main --allow-unrelated-histories
```

### Issue: Cannot push (permission denied)

```powershell
# Configure git credentials
git config --global user.name "[Your Name]"
git config --global user.email "[Your Email]"

# Get HF token: https://huggingface.co/settings/tokens
# Try push again - it will prompt for credentials
git push origin main
```

---

## 📞 Reference URLs

Keep handy:

```
GitHub Repo:
https://github.com/seritkutu-lab/hf-local-ai-space

Your HF Space:
https://huggingface.co/spaces/[username]/local-ai

HF Space Settings:
https://huggingface.co/spaces/[username]/local-ai/settings

ngrok Dashboard:
https://dashboard.ngrok.com/auth/your-authtoken

Your Deployed Space API:
https://[username]-local-ai.hf.space/api/chat
```

---

## ✨ Complete! What's Next?

✅ Done dengan deployment!

Sekarang:
1. Configure MetaGPT dengan HF Space URL
2. Test API with MetaGPT
3. Monitor HF Space logs jika ada issues
4. Update code di GitHub → auto-deploy ke HF

---

**Butuh bantuan?** Check:
- Detailed guide: `LANGKAH_3_DETAIL_SYNC_GITHUB.md`
- Troubleshooting: https://github.com/seritkutu-lab/hf-local-ai-space/blob/main/README.md
