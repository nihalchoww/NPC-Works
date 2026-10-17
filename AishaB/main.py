# main.py — Entry point for Anti-Gravity Birthday Bake-Off
#
# Supports both:
#   1. Native Pygame desktop application (`python main.py`)
#   2. Web preview & deployment (`app`, `application`, `handler` exports)

import os
import sys

# ─── Web / Serverless Entrypoints ──────────────────────────────────────────────
# Export top-level variables expected by web runners, WSGI/ASGI servers, and cloud hosts
from web_app import app, application, handler

__all__ = ["app", "application", "handler", "main"]


def run_desktop():
    """Launch the native Pygame desktop game window."""
    import pygame
    from settings import WIDTH, HEIGHT, SPACE_DARK
    from game import Game

    pygame.init()

    # Optional mixer init (graceful fallback if audio device unavailable)
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except Exception:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aisha's Birthday Bake-Off 🎂")

    clock = pygame.time.Clock()
    screen.fill(SPACE_DARK)
    pygame.display.flip()

    game = Game(screen, clock)

    try:
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
        sys.exit(0)


def run_web_server(port: int = 8080):
    """Run built-in HTTP server serving the playable web edition."""
    from wsgiref.simple_server import make_server
    print(f"Serving Aisha's Birthday Bake-Off on http://localhost:{port} ...")
    with make_server("0.0.0.0", port, application) as httpd:
        httpd.serve_forever()


def main():
    # If explicitly requested or PORT is set by cloud runner, run web server
    if "--web" in sys.argv or "PORT" in os.environ:
        port = int(os.environ.get("PORT", 8080))
        run_web_server(port)
        return

    # Attempt desktop display
    try:
        run_desktop()
    except Exception as e:
        # If no GUI display device (e.g., headless runner or cloud environment), fallback to web server
        if "No available video device" in str(e) or "cannot open display" in str(e).lower():
            port = int(os.environ.get("PORT", 8080))
            run_web_server(port)
        else:
            raise


if __name__ == "__main__":
    main()
