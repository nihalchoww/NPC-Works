# player.py — Catcher-style player for Anti-Gravity Birthday Bake-Off
#
# The girl moves LEFT / RIGHT only.
# She holds a tray ABOVE her head — that's the catch zone.
# Pixel-art: long black wavy hair, party hat, golden top, jeans, orange sneakers.

import math
import pygame
from settings import (
    WIDTH, HEIGHT, PLAYER_SPEED, TRAY_WIDTH, TRAY_HEIGHT,
    CYAN, PINK, PINK_LIGHT, WHITE, CREAM, OFF_WHITE,
    BROWN_DARK, GOLD, RED, ORANGE, PANEL_GREY, BLUE_BRIGHT,
)
from utils import clamp, alpha_surface


class Player:
    W = 60    # sprite bounding width
    H = 110   # sprite bounding height (includes raised tray arm)

    TRAY_Y_OFFSET = -50   # tray centre relative to player centre (above head)

    def __init__(self, x: float, y: float):
        self.x  = float(x)
        self.y  = float(y)
        self.vx = 0.0

        # Invincibility after hit
        self.invincible     = False
        self._inv_timer     = 0.0
        self._inv_duration  = 0.0
        self._flash         = False   # flicker state

        # Walk bob
        self._walk_t = 0.0

        self._surf = alpha_surface(self.W, self.H)
        self._render_sprite()

    # ── Public ────────────────────────────────────────────────────────────────

    def get_tray_rect(self) -> pygame.Rect:
        """Catch zone: the tray above the player's head."""
        tw, th = TRAY_WIDTH, TRAY_HEIGHT
        tx = int(self.x) - tw // 2
        ty = int(self.y) + self.TRAY_Y_OFFSET - th // 2
        return pygame.Rect(tx, ty, tw, th)

    def get_body_rect(self) -> pygame.Rect:
        """Player body rect (for obstacle collision)."""
        bw, bh = 32, 70
        return pygame.Rect(int(self.x) - bw // 2,
                           int(self.y) - 20,
                           bw, bh)

    def make_invincible(self, duration: float):
        self.invincible    = True
        self._inv_timer    = 0.0
        self._inv_duration = duration

    def update(self, dt: float, keys):
        # Horizontal movement
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            moving  = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            moving  = True
        else:
            self.vx = 0.0

        self.x = clamp(self.x + self.vx * dt,
                       self.W // 2, WIDTH - self.W // 2)

        # Walk animation
        if moving:
            self._walk_t += dt * 8.0

        # Invincibility timer
        if self.invincible:
            self._inv_timer += dt
            self._flash = int(self._inv_timer * 12) % 2 == 0
            if self._inv_timer >= self._inv_duration:
                self.invincible = False
                self._flash     = False

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        if self.invincible and self._flash:
            return   # flash invisible during invincibility

        ox, oy = offset
        cx = int(self.x) + ox
        cy = int(self.y) + oy

        # Slight walk bob
        bob = int(math.sin(self._walk_t) * 3)

        # Blit cached body sprite
        r = self._surf.get_rect(center=(cx, cy + bob))
        surface.blit(self._surf, r)

        # Draw tray (drawn fresh each frame so it stays at fixed position)
        self._draw_tray(surface, cx, cy + self.TRAY_Y_OFFSET + bob)

    # ── Private ───────────────────────────────────────────────────────────────

    def _render_sprite(self):
        """Draw the pixel-art girl onto self._surf once at init."""
        s  = self._surf
        cx = self.W // 2
        cy = self.H // 2 + 12   # shift down a bit so head is near top

        # ── Sneakers ──────────────────────────────────────────────────────────
        sneak = ORANGE
        pygame.draw.rect(s, sneak,  (cx - 18, cy + 36, 14, 10))   # left
        pygame.draw.rect(s, sneak,  (cx +  4, cy + 36, 14, 10))   # right
        pygame.draw.rect(s, (200, 90, 0), (cx - 20, cy + 42, 18, 5))  # sole L
        pygame.draw.rect(s, (200, 90, 0), (cx +  2, cy + 42, 18, 5))  # sole R
        # Lace dots
        for sx in [cx - 13, cx - 8, cx + 7, cx + 12]:
            pygame.draw.circle(s, WHITE, (sx, cy + 39), 2)

        # ── Jeans ─────────────────────────────────────────────────────────────
        jean = (70, 110, 180)
        pygame.draw.rect(s, jean, (cx - 16, cy + 10, 14, 28))   # left leg
        pygame.draw.rect(s, jean, (cx +  2, cy + 10, 14, 28))   # right leg
        # Seam line
        pygame.draw.line(s, (50, 80, 150), (cx - 2, cy + 10), (cx - 2, cy + 38), 2)

        # ── Torso — golden/beige top ───────────────────────────────────────────
        torso_col = (220, 180, 100)
        pygame.draw.rect(s, torso_col, (cx - 16, cy - 16, 32, 30))
        # Belt
        pygame.draw.rect(s, BROWN_DARK, (cx - 16, cy + 10, 32, 5))
        pygame.draw.rect(s, GOLD, (cx - 4, cy + 10, 8, 5))   # belt buckle
        # Collar V
        pygame.draw.polygon(s, (200, 160, 80),
                            [(cx - 6, cy - 16), (cx + 6, cy - 16), (cx, cy - 4)])
        # Sleeve stub left (arm raised — holding tray)
        pygame.draw.rect(s, torso_col, (cx - 24, cy - 36, 12, 26))   # raised L arm
        pygame.draw.rect(s, torso_col, (cx + 12, cy -  8, 12, 20))   # right arm

        # ── Head ──────────────────────────────────────────────────────────────
        skin = (190, 140, 95)
        pygame.draw.ellipse(s, skin, (cx - 14, cy - 50, 28, 32))

        # ── Long black wavy hair ───────────────────────────────────────────────
        hair = (20, 12, 8)
        # Crown mass
        pygame.draw.ellipse(s, hair, (cx - 15, cy - 57, 30, 22))
        # Long flowing left side
        for i, (hx, hy, hw, hh) in enumerate([
            (-18, cy - 42, 10, 18),
            (-20, cy - 28, 12, 20),
            (-19, cy - 10, 11, 22),
            (-17, cy +  8, 10, 18),
        ]):
            pygame.draw.ellipse(s, hair, (cx + hx, hy, hw, hh))
        # Right side shorter
        for (hx, hy, hw, hh) in [
            (10, cy - 42, 10, 16),
            (11, cy - 28, 9,  18),
            (10, cy - 12, 8,  14),
        ]:
            pygame.draw.ellipse(s, hair, (cx + hx, hy, hw, hh))

        # ── Headband / tiara ──────────────────────────────────────────────────
        pygame.draw.rect(s, PINK, (cx - 14, cy - 52, 28, 5))
        # Small gem
        pygame.draw.circle(s, CYAN, (cx, cy - 50), 4)
        pygame.draw.circle(s, WHITE, (cx - 1, cy - 51), 1)

        # ── Party hat ─────────────────────────────────────────────────────────
        hat_pts = [(cx + 2, cy - 70), (cx - 10, cy - 52), (cx + 14, cy - 52)]
        pygame.draw.polygon(s, PINK, hat_pts)
        pygame.draw.polygon(s, (200, 60, 140), hat_pts, 2)
        pygame.draw.rect(s, GOLD, (cx - 10, cy - 55, 24, 4))
        # Pom-pom
        pygame.draw.circle(s, WHITE, (cx + 2, cy - 71), 5)

        # ── Eyes ──────────────────────────────────────────────────────────────
        pygame.draw.circle(s, (25, 12, 5), (cx - 5, cy - 36), 4)
        pygame.draw.circle(s, (25, 12, 5), (cx + 5, cy - 36), 4)
        pygame.draw.circle(s, WHITE, (cx - 4, cy - 37), 1)
        pygame.draw.circle(s, WHITE, (cx + 6, cy - 37), 1)
        # Lashes
        pygame.draw.line(s, BROWN_DARK, (cx - 9, cy - 40), (cx - 5, cy - 38), 2)
        pygame.draw.line(s, BROWN_DARK, (cx + 5, cy - 40), (cx + 9, cy - 38), 2)

        # ── Smile ─────────────────────────────────────────────────────────────
        pygame.draw.arc(s, (150, 80, 40),
                        pygame.Rect(cx - 6, cy - 28, 12, 8),
                        math.pi + 0.4, 2 * math.pi - 0.4, 2)

    def _draw_tray(self, surface: pygame.Surface, cx: int, cy: int):
        """Draw the silver serving tray the player holds above her head."""
        tw = TRAY_WIDTH + 8
        th = TRAY_HEIGHT

        # Shadow / depth rim
        pygame.draw.ellipse(surface, (80, 85, 100),
                            (cx - tw // 2 - 2, cy - th // 2 + 2, tw + 4, th + 4))
        # Main tray
        pygame.draw.ellipse(surface, PANEL_GREY,
                            (cx - tw // 2, cy - th // 2, tw, th))
        # Highlight
        pygame.draw.ellipse(surface, (210, 215, 225),
                            (cx - tw // 2 + 4, cy - th // 2 + 2, tw - 14, th - 4))
        # Sheen
        pygame.draw.line(surface, WHITE,
                         (cx - tw // 2 + 8, cy - 2),
                         (cx + tw // 2 - 12, cy - 2), 2)
