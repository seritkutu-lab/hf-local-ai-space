#!/usr/bin/env python3
"""
Configuration settings untuk HF Space Local AI
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Server Configuration
# ============================================================

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 7860))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================================
# ngrok Configuration
# ============================================================

NGROK_ENABLED = os.getenv("NGROK_ENABLED", "False").lower() == "true"
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "")
NGROK_PUBLIC_URL = os.getenv("NGROK_PUBLIC_URL", "")

# ============================================================
# LLM Configuration
# ============================================================

# Local LLM model backend
LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")  # ollama, gpt4all, llama_cpp, huggingface

# Ollama Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# GPT4All Configuration
GPT4ALL_MODEL = os.getenv("GPT4ALL_MODEL", "mistral-7b.ggufv2.q4_0")
GPT4ALL_PATH = os.getenv("GPT4ALL_PATH", "./models")

# HuggingFace Configuration
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "gpt2")
HF_DEVICE = os.getenv("HF_DEVICE", "cpu")  # cpu, cuda, mps

# LLM Parameters
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 100))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", 0.95))
LLM_TOP_K = int(os.getenv("LLM_TOP_K", 50))

# ============================================================
# MetaGPT Configuration
# ============================================================

METAGPT_API_BASE = os.getenv("METAGPT_API_BASE", "")
METAGPT_API_KEY = os.getenv("METAGPT_API_KEY", "")
METAGPT_MODEL = os.getenv("METAGPT_MODEL", "local")

# ============================================================
# Security Configuration
# ============================================================

API_KEY_REQUIRED = os.getenv("API_KEY_REQUIRED", "False").lower() == "true"
API_KEY = os.getenv("API_KEY", "your-secret-key-here")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# ============================================================
# Database Configuration (optional)
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_ai.db")
ENABLE_PERSISTENCE = os.getenv("ENABLE_PERSISTENCE", "False").lower() == "true"

# ============================================================
# Helper Functions
# ============================================================

def get_config_summary() -> dict:
    """Get current configuration summary"""
    return {
        "server": {
            "host": HOST,
            "port": PORT,
            "debug": DEBUG
        },
        "ngrok": {
            "enabled": NGROK_ENABLED,
            "public_url": NGROK_PUBLIC_URL if NGROK_PUBLIC_URL else "Not active"
        },
        "llm": {
            "backend": LLM_BACKEND,
            "model": OLLAMA_MODEL if LLM_BACKEND == "ollama" else HF_MODEL_ID,
            "max_tokens": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE
        }
    }

def print_config():
    """Print current configuration"""
    import json
    print(json.dumps(get_config_summary(), indent=2))

if __name__ == "__main__":
    print_config()
