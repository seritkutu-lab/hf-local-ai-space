#!/usr/bin/env python3
"""
ngrok tunnel setup untuk HF Space Local AI
Untuk MetaGPT dan external access
"""

import os
import json
import logging
from typing import Optional, Dict
from dotenv import load_dotenv, set_key
from pyngrok import ngrok, conf
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class NgrokTunnel:
    """Manager untuk ngrok tunnels"""
    
    def __init__(self, ngrok_token: Optional[str] = None):
        """
        Initialize ngrok tunnel manager
        
        Args:
            ngrok_token: ngrok auth token. Jika None, ambil dari .env
        """
        self.ngrok_token = ngrok_token or os.getenv("NGROK_AUTH_TOKEN")
        self.tunnel = None
        self.public_url = None
        
        if self.ngrok_token:
            self._setup_ngrok()
        else:
            logger.warning("⚠️  NGROK_AUTH_TOKEN tidak ditemukan. Tunnel tidak akan tersedia.")
            logger.info("Get token dari: https://dashboard.ngrok.com/auth/your-authtoken")
    
    def _setup_ngrok(self):
        """Configure ngrok dengan auth token"""
        try:
            ngrok.set_auth_token(self.ngrok_token)
            logger.info("✅ ngrok auth token configured")
        except Exception as e:
            logger.error(f"❌ Error setting ngrok auth token: {str(e)}")
    
    def start_tunnel(self, port: int = 7860, proto: str = "http") -> Optional[str]:
        """
        Start ngrok tunnel ke specified port
        
        Args:
            port: Port yang akan di-tunnel
            proto: Protocol (http atau tcp)
        
        Returns:
            Public URL dari tunnel, atau None jika gagal
        """
        try:
            if not self.ngrok_token:
                logger.error("❌ ngrok token tidak tersedia")
                return None
            
            logger.info(f"🚀 Starting ngrok tunnel on {proto}://localhost:{port}")
            self.tunnel = ngrok.connect(port, proto=proto)
            self.public_url = self.tunnel.public_url
            
            logger.info(f"✅ ngrok tunnel started!")
            logger.info(f"🌐 Public URL: {self.public_url}")
            
            return self.public_url
        
        except Exception as e:
            logger.error(f"❌ Error starting ngrok tunnel: {str(e)}")
            return None
    
    def stop_tunnel(self):
        """Stop active tunnel"""
        try:
            if self.tunnel:
                ngrok.disconnect(self.public_url)
                logger.info(f"✅ Tunnel stopped: {self.public_url}")
                self.tunnel = None
                self.public_url = None
        except Exception as e:
            logger.error(f"Error stopping tunnel: {str(e)}")
    
    def get_status(self) -> Dict:
        """Get status dari semua active tunnels"""
        try:
            tunnels = ngrok.get_tunnels()
            return {
                "active": bool(self.public_url),
                "public_url": self.public_url,
                "all_tunnels": [
                    {
                        "name": tunnel.name,
                        "public_url": tunnel.public_url,
                        "proto": tunnel.proto
                    }
                    for tunnel in tunnels
                ]
            }
        except Exception as e:
            logger.error(f"Error getting tunnel status: {str(e)}")
            return {"error": str(e)}
    
    def save_url_to_env(self, env_file: str = ".env"):
        """Save public URL ke .env file untuk reference"""
        try:
            if self.public_url:
                set_key(env_file, "NGROK_PUBLIC_URL", self.public_url)
                logger.info(f"✅ Saved public URL to {env_file}")
        except Exception as e:
            logger.error(f"Error saving URL to env: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            tunnel = NgrokTunnel()
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 7860
            tunnel.start_tunnel(port=port)
            
            try:
                print("✅ Tunnel running. Press Ctrl+C to stop.")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                tunnel.stop_tunnel()
                print("\n✅ Tunnel stopped")
        
        elif command == "status":
            tunnel = NgrokTunnel()
            status = tunnel.get_status()
            print(json.dumps(status, indent=2))
        
        elif command == "stop":
            tunnel = NgrokTunnel()
            tunnel.stop_tunnel()
    else:
        print("Usage: python ngrok_setup.py [start|status|stop]")
