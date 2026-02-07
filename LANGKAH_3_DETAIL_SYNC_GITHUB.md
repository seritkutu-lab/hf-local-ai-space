# 🔄 LANGKAH 3 DETAIL: Sync dari GitHub ke HF Spaces (Feb 2026)

Panduan step-by-step yang detail untuk sync repository GitHub ke Hugging Face Spaces.

---

## 📌 OVERVIEW

Ada **2 metode utama** untuk sync dari GitHub ke HF Spaces di Feb 2026:

| Metode | Setup | Auto-Deploy | Speed | Recommended |
|--------|-------|-------------|-------|-------------|
| **Git Clone + Push** | Medium | ❌ Manual | Fast | ⭐ Beginner |
| **GitHub Actions Webhook** | Medium | ✅ Auto | Instant | ⭐ Advanced |

Aku kasih **METODE 1** (paling mudah) + **METODE 2** (paling otomatis).

---

## ⭐ METODE 1: Git Clone + Push (RECOMMENDED untuk Pemula)

Paling straightforward dan no setup kompleks.

### Step 1.1: Persiapan di Terminal

```powershell
# Di terminal baru (cek kamu di directory mana dulu)
cd $HOME
mkdir hf-spaces
cd hf-spaces
```

### Step 1.2: Clone HF Space Repository

Setelah buat HF Space (nama: `local-ai`), repository-nya pasti di HF Spaces Git.

```powershell
# Format: huggingface.co/spaces/[username]/[space-name]
# Contoh username: hasyiem, space: local-ai
# https://huggingface.co/spaces/hasyiem/local-ai

# Clone:
git clone https://huggingface.co/spaces/hasyiem/local-ai
cd local-ai
```

**Note**: Ganti `hasyiem` dengan username GitHub/HF kamu, dan `local-ai` dengan nama space kamu.

### Step 1.3: Ambil Files dari GitHub Repository

Ada 2 cara:

#### **CARA 1A: Download ZIP dari GitHub**

```powershell
# 1. Pergi ke: https://github.com/seritkutu-lab/hf-local-ai-space
# 2. Click tombol hijau "Code"
# 3. Click "Download ZIP"
# 4. Extract ZIP ke folder `local-ai` (overwrite jika ada)

# Via terminal (alternative):
curl -L https://github.com/seritkutu-lab/hf-local-ai-space/archive/refs/heads/main.zip -o hf-main.zip
tar -xf hf-main.zip
copy hf-local-ai-space-main\* .   # Move semua files
```

#### **CARA 1B: Use Git to Add Remote** (Lebih Pro)

```powershell
# Dalam folder `local-ai` yang sudah di-clone dari HF:

# Tambah upstream dari GitHub repo
git remote add github https://github.com/seritkutu-lab/hf-local-ai-space

# Pull files dari GitHub
git pull github main --allow-unrelated-histories

# Resolve conflicts jika ada (biasanya di README)
# Pilih "ours" untuk prefer GitHub version
```

### Step 1.4: Update .env File

```powershell
# Copy .env.example ke .env
copy .env.example .env

# Edit .env (gunakan notepad atau editor pilihan):
notepad .env

# Harus isi minimal:
# NGROK_AUTH_TOKEN=your_actual_token_here  # ⭐ WAJIB dari https://dashboard.ngrok.com
# NGROK_ENABLED=True
# LLM_BACKEND=ollama
```

### Step 1.5: Push ke HF Spaces

```powershell
# Review files yang bakal di-push
git status

# Add semua files
git add .

# Commit
git commit -m "Setup local AI space from GitHub repo"

# Push ke HF Spaces
git push origin main

# HF akan otomatis detect Dockerfile dan mulai build
```

### Step 1.6: Monitor Build

```powershell
# Check status di browser:
# https://huggingface.co/spaces/[username]/local-ai/settings

# Atau dari terminal, lihat logs:
git push -v   # Lihat verbose output

# Atau open di browser dan check "Logs" tab
```

Status yang akan kamu lihat:
- 🟡 **Building** - Proses Docker build running
- 🟠 **Building** - ~5-10 menit yang pertama kali
- 🟢 **Running** - SUCCESS! Space siap diakses
- 🔴 **Error** - Ada masalah, check logs

---

## 🚀 METODE 2: GitHub Actions untuk Auto-Deploy (Advanced)

Setiap push ke GitHub `main` branch, otomatis deploy ke HF Space.

### Step 2.1: Setup HF Token & Personal Access Token

Go ke: https://huggingface.co/settings/tokens

1. Click **Create new token**
2. Pilih:
   - **Name**: `hf-spaces-deploy`
   - **Token type**: **Fine-grained**
   - **Expiration**: 30 days (atau lebih lama)
   - **Permissions**: 
     - `write` untuk spaces
     - `read` untuk repo
3. Copy token → save tempat aman

### Step 2.2: Setup di GitHub Repository

Go ke: https://github.com/seritkutu-lab/hf-local-ai-space/settings/secrets/actions

1. Click **New repository secret**
2. Isi:
   - **Name**: `HF_TOKEN`
   - **Secret**: Paste HF token dari step 2.1
3. Click **Add secret**

Repeat untuk:
- **Name**: `HF_SPACE_REPO` 
- **Secret**: `hasyiem/local-ai` (format: username/space-name)

### Step 2.3: Create GitHub Actions Workflow

Di repository, buat file: `.github/workflows/deploy-to-hf.yml`

```yaml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Push to Hugging Face Space
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          HF_SPACE_REPO: ${{ secrets.HF_SPACE_REPO }}
        run: |
          git config --global user.email "action@github.com"
          git config --global user.name "GitHub Action"
          
          # Clone HF Space
          git clone https://hasyiem:$HF_TOKEN@huggingface.co/spaces/$HF_SPACE_REPO hf-space
          
          # Copy files (exclude .git)
          cp -r --exclude=.git --exclude=.github ../* hf-space/
          
          # Commit & push ke HF
          cd hf-space
          git add .
          git commit -m "Auto-deploy from GitHub ($(date))" || true
          git push https://hasyiem:$HF_TOKEN@huggingface.co/spaces/$HF_SPACE_REPO main
```

### Step 2.4: Trigger Deploy

```powershell
# Make any change & push
git add .
git commit -m "Test: trigger auto-deploy"
git push origin main

# GitHub Actions akan otomatis:
# 1. Trigger workflow
# 2. Clone HF Space repo
# 3. Copy files
# 4. Push ke HF Spaces
# 5. HF akan rebuild & deploy

# Monitor di: https://github.com/seritkutu-lab/hf-local-ai-space/actions
```

---

## 🔐 IMPORTANT: Configure Secrets di HF Spaces

Ini WAJIB, atau server tidak bisa connect ke ngrok!

### Di HF Spaces Settings:

1. Go ke: `https://huggingface.co/spaces/[username]/local-ai/settings`

2. Scroll ke **Secrets** section (atau **Repository Secrets**)

3. Click **Add Secret**

4. Isi:
   ```
   Name: NGROK_AUTH_TOKEN
   Value: [token dari https://dashboard.ngrok.com]
   ```

5. Click **Add secret**

Secret ini akan di-pass ke Docker container sebagai environment variable.

---

## ✅ Verifikasi Deploy Berhasil

Setelah build complete (status: 🟢 Running):

### Test 1: Health Check

```powershell
# Akses di browser atau terminal:
# https://[username]-local-ai.hf.space/health

# Atau via curl:
curl https://[username]-local-ai.hf.space/health

# Expected response:
# {"status":"healthy","service":"running"}
```

### Test 2: API Endpoint

```powershell
curl -X POST "https://[username]-local-ai.hf.space/api/chat" \
  -H "Content-Type: application/json" \
  -d '{\"prompt\": \"Test message\", \"max_tokens\": 50}'

# Expected response:
# {
#   \"response\": \"...\",
#   \"model\": \"local\",
#   \"tokens_used\": 5
# }
```

### Test 3: Web UI

Open di browser:
- `https://[username]-local-ai.hf.space/interface`

Harus bisa lihat Gradio chat interface. Try send message!

---

## 🛠️ Common Issues & Solutions

### ❌ Issue: "fatal: not a git repository"

**Cause**: Belum di-clone dari HF Spaces

**Solution**:
```powershell
cd /path/to/local-ai
git status  # Cek status
# Jika error, re-clone:
git clone https://huggingface.co/spaces/[username]/local-ai
```

---

### ❌ Issue: Space berstatus 🔴 ERROR saat build

**Check logs** di HF Spaces Settings → Logs tab

Usual causes:
- **Missing NGROK_AUTH_TOKEN secret** ← PALING SERING
- Bad `Dockerfile` syntax
- Missing dependencies di `requirements.txt`
- Environment variable conflict

**Solution**:
1. Add NGROK_AUTH_TOKEN secret (lihat section di atas)
2. Re-trigger build: Settings → Restart Space

---

### ❌ Issue: "Authentication failed" saat git push

**Cause**: GitHub/HF credentials tidak valid

**Solution**:
```powershell
# Setup Git credentials (one-time):
git config --global user.name "[Your Name]"
git config --global user.email "[Your Email]"

# For HF, gunakan PAT (Personal Access Token):
# https://huggingface.co/settings/tokens

# Clone dengan credentials:
git clone https://[username]:[hf_token]@huggingface.co/spaces/[username]/local-ai
```

---

### ❌ Issue: "remote: fatal: Not a valid object name"

**Cause**: Branch atau ref tidak ditemukan

**Solution**:
```powershell
# Ensure branch exist:
git branch -a

# Buat branch main jika belum ada:
git checkout -b main
git push -u origin main
```

---

## 📋 Step-by-Step Checklist

Gunakan untuk confirm setiap step:

```
PERSIAPAN:
□ Create HF Space (Docker SDK)
□ Get ngrok token dari https://dashboard.ngrok.com

METHOD 1 (Git Clone + Push):
□ Clone HF Space: git clone https://huggingface.co/spaces/[username]/[space]
□ cd ke folder space
□ Copy files dari GitHub repo
□ Edit .env dengan ngrok token
□ git add . && git commit && git push origin main
□ Wait untuk build complete (5-10 menit)

METHOD 2 (GitHub Actions Optional):
□ Create HF token di https://huggingface.co/settings/tokens
□ Add secrets di GitHub repo (HF_TOKEN, HF_SPACE_REPO)
□ Create .github/workflows/deploy-to-hf.yml
□ Trigger dengan push ke main branch

SECRETS CONFIGURATION:
□ Go to HF Space Settings
□ Add Secret: NGROK_AUTH_TOKEN = [your token]

VERIFICATION:
□ Check status: 🟢 Running
□ Test health: https://[username]-local-ai.hf.space/health
□ Test API: POST /api/chat
□ Open Web UI: /interface
□ Configure MetaGPT dengan HF Space URL
```

---

## 🎯 Next: Configure MetaGPT

Setelah Space running successfully, update MetaGPT config dengan:

```yaml
llm:
  api_type: custom
  base_url: https://[username]-local-ai.hf.space
  api_endpoint: /api/chat
  model: local
  temperature: 0.7
```

---

## 📞 Quick Reference Commands

```powershell
# Clone HF Space
git clone https://huggingface.co/spaces/[username]/local-ai

# Check git status
git status

# Pull latest dari GitHub
git pull github main --allow-unrelated-histories

# Push ke HF
git push origin main

# Check HF build logs (local terminal)
curl https://huggingface.co/api/spaces/[username]/local-ai/info

# Direct test API
wget --post-data='{\"prompt\":\"test\"}' ^\n  --header='Content-Type: application/json' ^\n  https://[username]-local-ai.hf.space/api/chat -O -
```

---

**Status**: Ready untuk Feb 2026 ✅  
**Last Updated**: 2026-02-08  
**Tested**: Git-based sync + Manual deploy
