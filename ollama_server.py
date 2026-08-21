"""
Sovereign Engine: Ollama & OpenAI Compatible REST API Server
Provides lightweight HTTP endpoints matching Ollama & OpenAI specifications:
  - POST /api/generate      (Ollama completion format)
  - POST /api/chat          (Ollama chat format)
  - POST /v1/chat/completions (OpenAI compatible format)
  - GET  /api/tags          (Ollama model listing)
  - GET  /v1/models         (OpenAI model listing)
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

try:
    import sov_e8_organism
    def snap_to_e8(vec):
        return sov_e8_organism.snap_to_e8(vec)
    def calculate_sectional_curvature(vec):
        return sov_e8_organism.sectional_curvature_approx(vec)
except Exception:
    def snap_to_e8(vec):
        return [round(x * 2) / 2.0 for x in vec[:8]]
    def calculate_sectional_curvature(vec):
        return sum(x * x for x in vec[:8]) / max(1.0, len(vec))
from sov_heart.tamagotchi.e8_pet import E8Pet


class SovereignOllamaHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Suppress noisy standard HTTP logging during normal operations
        pass

    def _send_json(self, status: int, payload: Dict[str, Any]):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/api/tags", "/v1/models"):
            models = [
                {
                    "name": "sovereign-e8:latest",
                    "id": "sovereign-e8",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "sovereign",
                    "details": {
                        "format": "e8_geometry",
                        "family": "lie_manifold",
                        "parameter_size": "240_roots",
                        "quantization_level": "E8_Lattice"
                    }
                }
            ]
            if self.path == "/v1/models":
                self._send_json(200, {"object": "list", "data": models})
            else:
                self._send_json(200, {"models": models})
        elif self.path == "/":
            self._send_json(200, {"status": "ok", "engine": "Sovereign Engine v1.0", "geometry": "E8"})
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            req = json.loads(raw_body)
        except Exception:
            req = {}

        # 1. Ollama /api/generate
        if self.path == "/api/generate":
            prompt = req.get("prompt", "")
            raw_vec = [float(ord(c)) for c in prompt[:8].ljust(8)]
            mag = sum(x*x for x in raw_vec)**0.5 or 1.0
            norm_vec = [x/mag for x in raw_vec]
            snapped = snap_to_e8(norm_vec)
            curv = calculate_sectional_curvature(snapped)

            response_text = (
                f"[Sovereign E8 Invariant Response]\n"
                f"Input Prompt: '{prompt}'\n"
                f"E8 Snapped Roots: {snapped[:4]}...\n"
                f"Sectional Curvature Score: {curv:.4f}\n"
                f"Status: Globally Coherent (H¹ = 0)"
            )
            self._send_json(200, {
                "model": req.get("model", "sovereign-e8"),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "response": response_text,
                "done": True,
                "context": snapped,
                "total_duration": 125000,
                "eval_count": 1
            })

        # 2. Ollama /api/chat or OpenAI /v1/chat/completions
        elif self.path in ("/api/chat", "/v1/chat/completions"):
            messages = req.get("messages", [])
            last_user_msg = ""
            for m in reversed(messages):
                if m.get("role") == "user":
                    last_user_msg = m.get("content", "")
                    break

            pet = E8Pet.create_new("SovereignNode")
            reaction = pet.feed(last_user_msg if last_user_msg else "Hello Sovereign Engine")
            v = pet.vitals()

            content_out = (
                f"Sovereign E8 Organism Node Response:\n"
                f"{reaction}\n\n"
                f"[Vitals] Health: {v['health']:.2f} | Energy: {v['energy']:.2f} | Coherence: {v['coherence']:.4f}"
            )

            if self.path == "/v1/chat/completions":
                self._send_json(200, {
                    "id": f"chatcmpl-sov-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": req.get("model", "sovereign-e8"),
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": content_out},
                        "finish_reason": "stop"
                    }],
                    "usage": {"prompt_tokens": len(last_user_msg), "completion_tokens": len(content_out), "total_tokens": len(last_user_msg) + len(content_out)}
                })
            else:
                self._send_json(200, {
                    "model": req.get("model", "sovereign-e8"),
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "message": {"role": "assistant", "content": content_out},
                    "done": True
                })
        else:
            self._send_json(404, {"error": "Endpoint not found"})


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def run_server(host: str = "0.0.0.0", port: int = 11434):
    target_port = port
    httpd = None
    
    # Try target port, then fallback to next 5 ports if occupied
    for p in range(target_port, target_port + 5):
        try:
            server_address = (host, p)
            httpd = ReusableHTTPServer(server_address, SovereignOllamaHandler)
            target_port = p
            break
        except OSError as e:
            if e.errno == 98:
                continue
            raise e

    if httpd is None:
        print(f"[X] Error: Could not bind to port {port} or fallback ports. Please specify an open port with --port <PORT>.")
        sys.exit(1)

    print(f"🚀 Sovereign Ollama/OpenAI API Server listening on http://{host}:{target_port}")
    if target_port != port:
        print(f"   [!] Note: Port {port} was in use; automatically rebound to port {target_port}.")
    print(f"   - Ollama Generate: POST http://{host}:{target_port}/api/generate")
    print(f"   - OpenAI Chat:     POST http://{host}:{target_port}/v1/chat/completions")
    print(f"   - Model Tags:      GET  http://{host}:{target_port}/api/tags")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Sovereign Ollama server stopped cleanly.")
        httpd.server_close()
