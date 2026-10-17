# main.py — Entry point for Anti-Gravity Birthday Bake-Off
#
# Usage:
#   pip install pygame
#   python main.py

import sys
import pygame
from settings import WIDTH, HEIGHT, FPS, SPACE_DARK
from game     import Game


def main():
    pygame.init()

    # Optional mixer init (graceful fallback if audio unavailable)
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except Exception:
        pass   # Game works fine without audio

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Anti-Gravity Birthday Bake-Off 🎂")

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


if __name__ == "__main__":
    main()
