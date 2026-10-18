# web_app.py — Web entrypoint & browser-playable edition of Aisha's Birthday Bake-Off
#
# Specially optimized for mobile phones (iOS & Android):
#   • Full PWA Native App: One-tap "Add to Home Screen" with custom Aisha icon
#   • 100% Offline Playable via Service Worker (sw.js)
#   • True Fullscreen Edge-to-Edge standalone display
#   • Responsive dynamic portrait & landscape canvas
#   • Direct smooth touch dragging & Phone Tilt Gyroscope Steering
#   • Virtual on-screen thumb buttons (◀, ▶, Action, Pause, Fullscreen, Tilt)
#   • iOS / Safari audio auto-unlock
#   • Haptic feedback (vibrations on catches, hits, and celebrations)
#   • Standard WSGI/ASGI & Serverless entrypoint for Vercel

import base64
import os

BASE_DIR = os.path.dirname(__file__)

def get_file_bytes(rel_path: str) -> bytes:
    p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p):
        with open(p, "rb") as f:
            return f.read()
    return b""

def get_file_text(rel_path: str) -> str:
    p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def handle_request(path: str = "/"):
    """Handle web HTTP request and serve static PWA assets or game HTML."""
    clean_path = path.split("?")[0].rstrip("/")
    if not clean_path:
        clean_path = "/"

    if clean_path == "/manifest.json":
        data = get_file_bytes("manifest.json")
        return data, "application/manifest+json; charset=utf-8"

    if clean_path == "/sw.js":
        data = get_file_bytes("sw.js")
        return data, "application/javascript; charset=utf-8"

    if clean_path in ("/icon-192.png", "/assets/icon-192.png"):
        data = get_file_bytes("icon-192.png") or get_file_bytes("assets/icon-192.png")
        return data, "image/png"

    if clean_path in ("/icon-512.png", "/assets/icon-512.png"):
        data = get_file_bytes("icon-512.png") or get_file_bytes("assets/icon-512.png")
        return data, "image/png"

    if clean_path in ("/apple-touch-icon.png", "/assets/apple-touch-icon.png", "/apple-touch-icon-precomposed.png"):
        data = get_file_bytes("apple-touch-icon.png") or get_file_bytes("assets/apple-touch-icon.png")
        return data, "image/png"

    if clean_path in ("/favicon.png", "/assets/favicon.png"):
        data = get_file_bytes("favicon.png") or get_file_bytes("assets/favicon.png")
        if data:
            return data, "image/png"
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>'
        return svg.encode("utf-8"), "image/svg+xml"

    if clean_path == "/favicon.ico":
        data = get_file_bytes("favicon.png") or get_file_bytes("assets/favicon.png")
        if data:
            return data, "image/png"
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>'
        return svg.encode("utf-8"), "image/svg+xml"

    # Default: serve latest game.html
    html_content = get_file_text("game.html")
    return html_content.encode("utf-8"), "text/html; charset=utf-8"


def app(environ, start_response):
    """
    Standard WSGI Application callable(environ, start_response).
    Fully compatible with Vercel Python runtime, Gunicorn, uWSGI, and wsgiref.
    """
    path = environ.get("PATH_INFO", "/")
    body, content_type = handle_request(path)
    start_response("200 OK", [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-cache" if "text/html" in content_type else "public, max-age=86400"),
    ])
    return [body]


application = app


def handler(event, context=None):
    """Serverless AWS Lambda / Vercel entrypoint."""
    path = "/"
    if isinstance(event, dict):
        path = event.get("rawPath") or event.get("path") or "/"
    body, content_type = handle_request(path)
    is_binary = content_type.startswith("image/")
    if is_binary:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": content_type,
                "Content-Length": str(len(body)),
                "Cache-Control": "public, max-age=86400",
            },
            "isBase64Encoded": True,
            "body": base64.b64encode(body).decode("ascii"),
        }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": content_type,
            "Content-Length": str(len(body)),
            "Cache-Control": "no-cache",
        },
        "body": body.decode("utf-8", errors="replace"),
    }
