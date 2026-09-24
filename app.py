"""Small dependency-free web server for the West Africa capitals quiz."""
import json
import os
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
COUNTRIES = [
    ("Benin", "Porto-Novo", "Cotonou is the seat of government."),
    ("Burkina Faso", "Ouagadougou", ""),
    ("Cabo Verde", "Praia", ""),
    ("Côte d’Ivoire", "Yamoussoukro", "Abidjan remains the main economic centre."),
    ("The Gambia", "Banjul", ""),
    ("Ghana", "Accra", ""),
    ("Guinea", "Conakry", ""),
    ("Guinea-Bissau", "Bissau", ""),
    ("Liberia", "Monrovia", ""),
    ("Mali", "Bamako", ""),
    ("Mauritania", "Nouakchott", ""),
    ("Niger", "Niamey", ""),
    ("Nigeria", "Abuja", ""),
    ("Senegal", "Dakar", ""),
    ("Sierra Leone", "Freetown", ""),
    ("Togo", "Lomé", ""),
]
BY_NAME = {name: (capital, fact) for name, capital, fact in COUNTRIES}
CAPITALS = [capital for _, capital, _ in COUNTRIES]


def question():
    name, capital, _ = random.choice(COUNTRIES)
    options = random.sample([x for x in CAPITALS if x != capital], 3) + [capital]
    random.shuffle(options)
    return {"country": name, "options": options}


class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, value):
        self.send_bytes(status, json.dumps(value, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/question":
            return self.send_json(200, question())
        if path == "/health":
            return self.send_json(200, {"status": "ok"})
        files = {"/": ("index.html", "text/html"), "/style.css": ("style.css", "text/css"), "/app.js": ("app.js", "text/javascript")}
        if path not in files:
            return self.send_json(404, {"error": "Not found"})
        filename, mime = files[path]
        self.send_bytes(200, (ROOT / "static" / filename).read_bytes(), mime + "; charset=utf-8")

    def do_POST(self):
        if urlparse(self.path).path != "/api/answer":
            return self.send_json(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1024 or length <= 0:
                raise ValueError("Invalid length")
            data = json.loads(self.rfile.read(length))
            name, choice = data["country"], data["choice"]
            if name not in BY_NAME or choice not in CAPITALS:
                raise ValueError("Invalid answer")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return self.send_json(400, {"error": "Invalid answer"})
        capital, fact = BY_NAME[name]
        self.send_json(200, {"correct": choice == capital, "capital": capital, "fact": fact})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Quiz listening on port {port}", flush=True)
    server.serve_forever()
