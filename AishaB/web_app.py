# web_app.py — Web entrypoint & browser-playable edition of Aisha's Birthday Bake-Off
#
# Specially optimized for mobile phones (iOS & Android):
#   • Responsive dynamic portrait & landscape canvas (full edge-to-edge screen)
#   • Direct smooth touch dragging (glide finger to steer Aisha)
#   • Virtual on-screen thumb buttons (◀, ▶, Action, Pause, Fullscreen)
#   • iOS / Safari audio auto-unlock
#   • Haptic feedback (vibrations on catches, hits, and celebrations)
#   • Aisha's photo embedded as instant data URI (100% offline, zero network lag)
#   • Standard WSGI/ASGI entrypoint for Vercel

import os

HTML_FILE = os.path.join(os.path.dirname(__file__), "game.html")
with open(HTML_FILE, "r", encoding="utf-8") as _f:
    HTML_CONTENT = _f.read()


def handle_request(path: str = "/"):
    """Handle web HTTP request."""
    if path in ("/favicon.ico", "/favicon.png"):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>'
        return svg.encode("utf-8"), "image/svg+xml"
    return HTML_CONTENT.encode("utf-8"), "text/html; charset=utf-8"


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
    ])
    return [body]


application = app


def handler(event, context=None):
    """Serverless AWS Lambda / Vercel entrypoint."""
    path = "/"
    if isinstance(event, dict):
        path = event.get("rawPath") or event.get("path") or "/"
    body, content_type = handle_request(path)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": content_type,
            "Content-Length": str(len(body)),
        },
        "body": body.decode("utf-8", errors="replace"),
    }
