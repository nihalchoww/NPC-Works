# player.py — Catcher-style player for Aisha's Birthday Bake-Off
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

        # ── Torso — Aisha's cream & red floral blouse with apron ──────────────
        blouse_col = (245, 238, 225)
        apron_col  = (225, 180, 105)
        pygame.draw.rect(s, blouse_col, (cx - 16, cy - 16, 32, 28))
        # Signature red floral petal patterns from Aisha's blouse
        for fx, fy in [(cx - 9, cy - 10), (cx + 7, cy - 8), (cx - 6, cy + 2), (cx + 8, cy + 4)]:
            pygame.draw.circle(s, (190, 50, 40), (fx, fy), 2)
        # Golden baking apron
        pygame.draw.rect(s, apron_col, (cx - 12, cy - 6, 24, 18))
        # Belt
        pygame.draw.rect(s, BROWN_DARK, (cx - 16, cy + 10, 32, 5))
        pygame.draw.rect(s, GOLD, (cx - 4, cy + 10, 8, 5))   # belt buckle

        # Raised arms holding the tray
        arm_col = (220, 175, 130)
        pygame.draw.line(s, arm_col, (cx - 14, cy - 6), (cx - 24, cy - 42), 4)
        pygame.draw.line(s, arm_col, (cx + 14, cy - 6), (cx + 24, cy - 42), 4)

        # ── Head — Aisha's Photo Attachment ───────────────────────────────────
        head_attached = False
        import os
        head_path = os.path.join(os.path.dirname(__file__), "assets", "aisha_head.png")
        if os.path.exists(head_path):
            try:
                head_surf = pygame.image.load(head_path).convert_alpha()
                head_scaled = pygame.transform.smoothscale(head_surf, (44, 48))
                s.blit(head_scaled, (cx - 22, cy - 54))
                head_attached = True
            except Exception:
                pass

        if not head_attached:
            # Procedural fallback
            skin = (190, 140, 95)
            pygame.draw.ellipse(s, skin, (cx - 14, cy - 50, 28, 32))
            hair = (20, 12, 8)
            pygame.draw.ellipse(s, hair, (cx - 15, cy - 57, 30, 22))
            # Pink butterfly clip
            pygame.draw.rect(s, PINK, (cx + 3, cy - 48, 6, 5))
            # Eyes & Smile
            pygame.draw.circle(s, (25, 12, 5), (cx - 5, cy - 36), 3)
            pygame.draw.circle(s, (25, 12, 5), (cx + 5, cy - 36), 3)
            pygame.draw.arc(s, (150, 80, 40),
                            pygame.Rect(cx - 6, cy - 28, 12, 8),
                            math.pi + 0.4, 2 * math.pi - 0.4, 2)

        # ── Birthday party hat on top of hair ─────────────────────────────────
        hat_pts = [(cx + 2, cy - 68), (cx - 9, cy - 52), (cx + 13, cy - 52)]
        pygame.draw.polygon(s, PINK, hat_pts)
        pygame.draw.polygon(s, (200, 60, 140), hat_pts, 1)
        pygame.draw.rect(s, GOLD, (cx - 9, cy - 54, 22, 3))
        pygame.draw.circle(s, WHITE, (cx + 2, cy - 69), 3)

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
