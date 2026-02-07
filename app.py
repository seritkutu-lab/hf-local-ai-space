#!/usr/bin/env python3
"""
Hugging Face Space - Local AI with ngrok tunnel support
Compatible with MetaGPT integration
"""

import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv
import gradio as gr
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# ============================================================
# FastAPI Backend
# ============================================================

app = FastAPI(title="Local AI Server", version="1.0.0")

class QueryRequest(BaseModel):
    """Request model untuk AI queries"""
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    model: Optional[str] = "local"

class QueryResponse(BaseModel):
    """Response model untuk AI queries"""
    response: str
    model: str
    tokens_used: int

# Simulated LLM response (ganti dengan model lokal sesuai kebutuhan)
def get_ai_response(prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
    """
    Fungsi untuk mendapatkan response dari model lokal
    Bisa diganti dengan:
    - LLaMA via ollama
    - GPT4All
    - Llama.cpp
    - Custom model
    """
    # Contoh: integrated dengan Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature
                }
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "Error: no response")
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        # Fallback jika ollama tidak running
        return f"Response yang dummy: '{prompt}' - Pastikan Ollama/model lokal sudah running di localhost:11434"
    except Exception as e:
        logger.error(f"Error in get_ai_response: {str(e)}")
        return f"Error: {str(e)}"

# FastAPI Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Local AI Server",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health",
            "gradio_ui": "/interface"
        }
    }

@app.get("/health")
async def health_check():
    """Health check untuk monitoring"""
    return {"status": "healthy", "service": "running"}

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest) -> QueryResponse:
    """
    Main chat endpoint untuk MetaGPT integration
    
    Usage:
    POST /api/chat
    {
        "prompt": "What is machine learning?",
        "max_tokens": 100,
        "temperature": 0.7,
        "model": "local"
    }
    """
    try:
        if not request.prompt or len(request.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt tidak boleh kosong")
        
        response = get_ai_response(
            prompt=request.prompt,
            max_tokens=request.max_tokens or 100,
            temperature=request.temperature or 0.7
        )
        
        return QueryResponse(
            response=response,
            model=request.model or "local",
            tokens_used=len(response.split())
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# Gradio Interface
# ============================================================

def gradio_chat(message: str, history):
    """Interface untuk Gradio ChatBot"""
    response = get_ai_response(message)
    return response

# Create Gradio ChatInterface
chat_interface = gr.ChatInterface(
    fn=gradio_chat,
    title="🤖 Local AI Chat",
    description="Interface untuk local AI model dengan ngrok tunnel support",
    theme=gr.themes.Soft(),
    examples=[
        "Apa itu machine learning?",
        "Jelaskan tentang deep learning",
        "Bagaimana cara menggunakan API ini untuk MetaGPT?"
    ]
)

# ============================================================
# Mount Gradio ke FastAPI
# ============================================================

# Combine FastAPI dengan Gradio
gr.mount_gradio_app(app, chat_interface, path="/interface")

# ============================================================
# Main entry point
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    # Get port dari environment atau default 7860
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info("API docs available at http://localhost:{port}/docs")
    logger.info("Gradio interface available at http://localhost:{port}/interface")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
