"""로컬 시안 서버. 실행: python -m src.app (외부 패키지 설치 불필요)."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .quiz import CHOICES, CITY_TYPES, QUESTIONS, calculate_result

STATIC = Path(__file__).resolve().parent.parent / "static"
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/script.js": ("script.js", "text/javascript; charset=utf-8"),
    "/city.svg": ("city.svg", "image/svg+xml"),
}


class AppHandler(BaseHTTPRequestHandler):
    """HTTP와 화면 제공 부분. 과제의 핵심 Python 문법은 quiz.py에 있습니다."""

    def send_body(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_body(status, body, "application/json; charset=utf-8")

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/quiz":
            self.send_json(200, {"questions": QUESTIONS, "choices": CHOICES, "types": CITY_TYPES})
        elif path in FILES:
            filename, content_type = FILES[path]
            self.send_body(200, (STATIC / filename).read_bytes(), content_type)
        else:
            self.send_json(404, {"error": "페이지를 찾을 수 없습니다."})

    def do_POST(self):
        if urlsplit(self.path).path != "/api/result":
            self.send_json(404, {"error": "페이지를 찾을 수 없습니다."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                raise ValueError("요청 크기가 올바르지 않습니다.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("응답 형식이 올바르지 않습니다.")
            self.send_json(200, calculate_result(payload.get("answers")))
        except (ValueError, UnicodeDecodeError) as error:
            self.send_json(400, {"error": str(error)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CITY:FIT 로컬 미리보기")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), AppHandler)
    print(f"CITY:FIT preview: http://localhost:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.")
    finally:
        server.server_close()
