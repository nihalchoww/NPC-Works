# ui.py — HUD, backgrounds and screens for Anti-Gravity Birthday Bake-Off
#
# Visual style matches the reference image:
#   • Space / galaxy background visible through portholes
#   • Cockpit blue walls with rivets
#   • HAPPY BIRTHDAY bunting across top
#   • Confetti raining down constantly
#   • HUD: SCORE | HI-SCORE at top, timer centre, LIVES top-right,
#           LIVES+hearts bottom-left, ZERO-G MODE bottom-centre, STAGE N bottom-right
#   • Heart lives display

import math, random, os
import pygame
from settings import (
    WIDTH, HEIGHT,
    SPACE_DARK, SPACE_MID, COCKPIT_BLUE, COCKPIT_DARK, COCKPIT_MID,
    PANEL_GREY, BOLT_GREY, GALAXY_PURPLE, GALAXY_PINK,
    CYAN, CYAN_DIM, PINK, PINK_LIGHT, PINK_DARK, GOLD, GOLD_DIM,
    RED, RED_BRIGHT, ORANGE, WHITE, OFF_WHITE,
    GREEN, PURPLE, BLUE_BRIGHT,
    BALLOON_COLORS, BUNTING_COLORS, CONFETTI_COLORS,
)
from utils import draw_text, draw_text_glow, draw_star, alpha_surface, get_font


# ─── Starfield ─────────────────────────────────────────────────────────────────
class Starfield:
    LAYER_SPEEDS = [0.08, 0.25, 0.60]
    LAYER_SIZES  = [1, 2, 3]
    LAYER_COUNTS = [90, 70, 40]

    def __init__(self):
        self.stars = []
        for layer in range(3):
            layer_stars = []
            for _ in range(self.LAYER_COUNTS[layer]):
                layer_stars.append([random.randint(0, WIDTH),
                                    random.randint(0, HEIGHT),
                                    random.randint(120, 255)])
            self.stars.append(layer_stars)
        self._t = 0.0

    def update(self, dt):
        self._t += dt
        for li, layer in enumerate(self.stars):
            for star in layer:
                star[0] -= self.LAYER_SPEEDS[li]
                if star[0] < 0:
                    star[0] = WIDTH
                    star[1] = random.randint(0, HEIGHT)

    def draw(self, surface):
        for li, layer in enumerate(self.stars):
            sz = self.LAYER_SIZES[li]
            for star in layer:
                b = int(star[2] * (0.65 + 0.35 * math.sin(self._t * 2.5 + star[0])))
                b = max(50, min(255, b))
                col = (b, b, b)
                if sz == 1:
                    surface.set_at((int(star[0]), int(star[1])), col)
                else:
                    pygame.draw.circle(surface, col,
                                       (int(star[0]), int(star[1])), sz)


# ─── Galaxy swirl (for porthole interior) ─────────────────────────────────────
def _draw_galaxy(surface, cx, cy, r, t):
    """Draw a tiny pixel-art galaxy inside a porthole."""
    # Deep space fill already done via circle clip
    # Galaxy centre glow
    pygame.draw.circle(surface, (160, 80, 200), (cx, cy), r // 3)
    pygame.draw.circle(surface, (200, 120, 240), (cx, cy), r // 6)
    # Arm dots
    for i in range(22):
        angle = 2 * math.pi * i / 22 + t * 0.4
        dist  = r * 0.25 + r * 0.5 * (i / 22)
        px    = cx + int(dist * math.cos(angle))
        py    = cy + int(dist * math.sin(angle) * 0.5)
        bri   = random.randint(130, 220)
        pygame.draw.circle(surface, (bri, bri // 2, bri), (px, py), 1)


# ─── Balloon ───────────────────────────────────────────────────────────────────
class _Balloon:
    def __init__(self):
        self.x     = float(random.randint(30, WIDTH - 30))
        self.y     = float(random.randint(-HEIGHT, HEIGHT))
        self.color = random.choice(BALLOON_COLORS)
        self.dy    = random.uniform(-0.30, -0.14)
        self.w     = random.uniform(1.8, 2.8)
        self.sz    = random.randint(16, 28)
        self._t    = random.uniform(0, math.pi * 2)

    def update(self, dt):
        self._t += dt * 2.2
        self.y  += self.dy
        self.x  += math.sin(self._t) * 0.25
        if self.y < -60:
            self.y = HEIGHT + 30
            self.x = random.randint(30, WIDTH - 30)

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.sz
        pygame.draw.ellipse(surface, self.color,
                            (cx - r, cy - int(r * 1.35), r * 2, int(r * 2.7)))
        # Shine
        sc = tuple(min(255, c + 70) for c in self.color)
        pygame.draw.ellipse(surface, sc,
                            (cx - r // 2, cy - int(r * 1.2), r // 2, r // 2))
        # String
        pygame.draw.line(surface, (160, 160, 180),
                         (cx, cy + int(r * 1.35)),
                         (cx + 5, cy + int(r * 1.35) + 18), 1)


class BalloonLayer:
    def __init__(self, n=10):
        self.balloons = [_Balloon() for _ in range(n)]

    def update(self, dt):
        for b in self.balloons: b.update(dt)

    def draw(self, surface):
        for b in self.balloons: b.draw(surface)


# ─── Cockpit background ────────────────────────────────────────────────────────
def draw_cockpit_background(surface: pygame.Surface, starfield: Starfield,
                             t: float = 0.0, offset=(0, 0)):
    """
    Space-kitchen cockpit matching the reference image:
    - Deep space dark background
    - Side wall panels (cockpit blue) with rivets
    - Two large porthole windows on each side showing galaxy
    - Floor panel at the bottom
    - Thin top strip
    """
    ox, oy = offset
    surface.fill(SPACE_DARK)

    # ── Porthole windows ──────────────────────────────────────────────────────
    porthole_specs = [
        (200, 300, 120),   # left large
        (WIDTH - 200, 300, 120),  # right large
        (140, 540, 70),   # left small
        (WIDTH - 140, 540, 70),   # right small
    ]
    for wx, wy, wr in porthole_specs:
        cx_w, cy_w = wx + ox, wy + oy
        # Space interior
        pygame.draw.circle(surface, SPACE_MID, (cx_w, cy_w), wr)
        # Galaxy swirl
        _draw_galaxy(surface, cx_w, cy_w, wr, t)
        # Starfield dots inside
        starfield.draw(surface)
        # Porthole rim
        pygame.draw.circle(surface, COCKPIT_MID,   (cx_w, cy_w), wr, 8)
        pygame.draw.circle(surface, BOLT_GREY,     (cx_w, cy_w), wr + 10, 4)
        pygame.draw.circle(surface, COCKPIT_DARK,  (cx_w, cy_w), wr + 14, 3)
        # Bolts at N/S/E/W
        for ba in [0, math.pi/2, math.pi, 3*math.pi/2]:
            bx = cx_w + int((wr + 12) * math.cos(ba))
            by = cy_w + int((wr + 12) * math.sin(ba))
            pygame.draw.circle(surface, BOLT_GREY, (bx, by), 5)
            pygame.draw.circle(surface, PANEL_GREY, (bx, by), 3)

    # ── Left / right wall panels ───────────────────────────────────────────────
    for px, pw in [(0, 130), (WIDTH - 130, 130)]:
        pygame.draw.rect(surface, COCKPIT_DARK, (px + ox, 0 + oy, pw, HEIGHT))
    # Inner edge line
    for px in [130, WIDTH - 130]:
        pygame.draw.line(surface, COCKPIT_MID,
                         (px + ox, 0 + oy), (px + ox, HEIGHT + oy), 3)

    # ── Top panel strip ────────────────────────────────────────────────────────
    pygame.draw.rect(surface, COCKPIT_BLUE, (0 + ox, 0 + oy, WIDTH, 58))
    pygame.draw.rect(surface, COCKPIT_MID,  (0 + ox, 55 + oy, WIDTH, 4))

    # ── Floor panel ────────────────────────────────────────────────────────────
    pygame.draw.rect(surface, COCKPIT_DARK,  (0 + ox, HEIGHT - 52 + oy, WIDTH, 52))
    pygame.draw.rect(surface, COCKPIT_MID,   (0 + ox, HEIGHT - 52 + oy, WIDTH, 4))

    # ── Rivets along top strip ─────────────────────────────────────────────────
    for rx in range(140, WIDTH - 135, 48):
        for ry in [10, 48]:
            pygame.draw.circle(surface, BOLT_GREY, (rx + ox, ry + oy), 4)
            pygame.draw.circle(surface, PANEL_GREY, (rx + ox, ry + oy), 2)

    # ── Panel rivets on sides ─────────────────────────────────────────────────
    for ry in range(80, HEIGHT - 60, 50):
        for rx in [118, WIDTH - 118]:
            pygame.draw.circle(surface, BOLT_GREY, (rx + ox, ry + oy), 4)
            pygame.draw.circle(surface, PANEL_GREY, (rx + ox, ry + oy), 2)


# ─── Bunting banner ────────────────────────────────────────────────────────────
def draw_bunting(surface: pygame.Surface, t: float, offset=(0, 0)):
    """'HAPPY BIRTHDAY!' triangular flag bunting across the play area top."""
    ox, oy = offset
    letters  = "HAPPY BIRTHDAY!"
    letters  = [c for c in letters if c != ' '] + [' ']
    # Use the non-space chars
    letters  = list("HAPPYBIRTHDAY!")
    n        = len(letters)
    x_start  = 134
    x_end    = WIDTH - 134
    y_base   = 66

    # String
    pts = []
    for i in range(n + 2):
        px   = x_start + (x_end - x_start) * i / (n + 1)
        sag  = math.sin(math.pi * i / (n + 1)) * 16
        sway = math.sin(t * 1.4 + i * 0.35) * 2
        pts.append((int(px) + ox, int(y_base + sag + sway) + oy))
    if len(pts) >= 2:
        pygame.draw.lines(surface, (160, 140, 100), False, pts, 2)

    # Flags
    fw = (x_end - x_start) // (n - 1)
    for i, letter in enumerate(letters):
        fx   = x_start + fw * i
        sag  = math.sin(math.pi * (i + 1) / (n + 1)) * 16
        sway = math.sin(t * 1.4 + i * 0.35) * 2
        fy   = y_base + sag + sway

        col  = BUNTING_COLORS[i % len(BUNTING_COLORS)]
        tipy = fy + 30
        fpts = [
            (int(fx - 11) + ox, int(fy) + oy),
            (int(fx + 11) + ox, int(fy) + oy),
            (int(fx)      + ox, int(tipy) + oy),
        ]
        pygame.draw.polygon(surface, col, fpts)
        pygame.draw.polygon(surface, WHITE, fpts, 1)
        font  = get_font(12)
        lsurf = font.render(letter, False, WHITE)
        lr    = lsurf.get_rect(center=(int(fx) + ox, int(fy) + 11 + oy))
        surface.blit(lsurf, lr)


# ─── HUD ───────────────────────────────────────────────────────────────────────
class HUD:
    """Draws all HUD elements to match the reference image layout."""

    def __init__(self):
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface: pygame.Surface, score: int, hi_score: int,
             lives: int, max_lives: int, time_left: float,
             stage: int, total_stages: int):

        self._draw_top_bar(surface, score, hi_score, lives, max_lives, time_left)
        self._draw_bottom_bar(surface, lives, max_lives, stage, total_stages)

    # ── Top bar ───────────────────────────────────────────────────────────────
    def _draw_top_bar(self, surface, score, hi_score, lives, max_lives, time_left):
        # Background already provided by cockpit top strip

        # SCORE (top-left)
        draw_text(surface, "SCORE:", 18, GOLD_DIM, 14, 6, shadow=True)
        draw_text(surface, f"{score:06d}", 26, GOLD, 14, 26,
                  shadow=True, shadow_color=(80, 50, 0))

        # HI-SCORE (top-centre)
        draw_text(surface, "HI-SCORE:", 18, GOLD_DIM,
                  WIDTH // 2, 6, anchor="midtop", shadow=True)
        draw_text(surface, f"{hi_score:06d}", 26, GOLD,
                  WIDTH // 2, 26, anchor="midtop",
                  shadow=True, shadow_color=(80, 50, 0))

        # LIVES hearts (top-right)
        draw_text(surface, "LIVES", 18, GOLD_DIM, WIDTH - 14, 6,
                  anchor="topright", shadow=True)
        hx = WIDTH - 14 - (max_lives * 28)
        for i in range(max_lives):
            col = RED_BRIGHT if i < lives else (80, 30, 30)
            self._draw_heart(surface, hx + i * 28 + 14, 36, 11, col)

        # ZERO-G badge (top-right box)
        bw, bh = 90, 26
        bx = WIDTH - bw - 8
        by = 6
        pygame.draw.rect(surface, COCKPIT_DARK, (bx, by, bw, bh))
        pygame.draw.rect(surface, CYAN, (bx, by, bw, bh), 2)
        draw_text(surface, "ZERO-G", 16, CYAN, bx + bw // 2, by + bh // 2,
                  anchor="center")

        # Timer (centre box)
        secs = max(0, int(time_left))
        mm   = secs // 60
        ss   = secs % 60
        tstr = f"{mm}:{ss:02d}"
        # Box
        tw, th = 100, 40
        tx = WIDTH // 2 - tw // 2
        ty = 8
        pygame.draw.rect(surface, (20, 60, 140), (tx, ty, tw, th))
        pygame.draw.rect(surface, CYAN, (tx, ty, tw, th), 2)
        if time_left < 10:
            tcol = RED_BRIGHT if int(self._t * 4) % 2 == 0 else WHITE
        else:
            tcol = WHITE
        draw_text(surface, tstr, 26, tcol, WIDTH // 2, ty + th // 2,
                  anchor="center", shadow=True)

    # ── Bottom bar ────────────────────────────────────────────────────────────
    def _draw_bottom_bar(self, surface, lives, max_lives, stage, total_stages):
        y_base = HEIGHT - 50

        # LIVES hearts (bottom-left)
        draw_text(surface, "LIVES", 16, WHITE, 14, y_base + 4, shadow=True)
        for i in range(max_lives):
            col = RED_BRIGHT if i < lives else (80, 30, 30)
            self._draw_heart(surface, 22 + i * 28, y_base + 30, 10, col)

        # ZERO-G MODE (bottom-centre box)
        bw, bh = 220, 38
        bx = WIDTH // 2 - bw // 2
        by = y_base + 6
        pulse = 0.55 + 0.45 * math.sin(self._t * 3.5)
        bg    = (int(20 * pulse), int(50 * pulse), int(120 * pulse))
        pygame.draw.rect(surface, bg, (bx, by, bw, bh))
        pygame.draw.rect(surface, CYAN, (bx, by, bw, bh), 2)
        ccol = (int(0), int(200 * pulse), int(255 * pulse))
        draw_text(surface, "ZERO-G  MODE", 20, ccol,
                  WIDTH // 2, by + bh // 2, anchor="center")

        # STAGE (bottom-right box)
        sw, sh = 160, 38
        sx = WIDTH - sw - 10
        sy = y_base + 6
        pygame.draw.rect(surface, COCKPIT_DARK, (sx, sy, sw, sh))
        pygame.draw.rect(surface, GOLD, (sx, sy, sw, sh), 2)
        draw_text(surface, f"STAGE  {stage}", 20, GOLD,
                  sx + sw // 2, sy + sh // 2, anchor="center",
                  shadow=True, shadow_color=(60, 40, 0))

    # ── Heart shape ───────────────────────────────────────────────────────────
    @staticmethod
    def _draw_heart(surface, cx, cy, r, color):
        """Draw a pixel heart at (cx, cy) with radius r."""
        pygame.draw.circle(surface, color, (cx - r // 2, cy - r // 4), r // 2)
        pygame.draw.circle(surface, color, (cx + r // 2, cy - r // 4), r // 2)
        pts = [(cx - r, cy),
               (cx,     cy + r),
               (cx + r, cy)]
        pygame.draw.polygon(surface, color, pts)


# ─── Stage Clear overlay ───────────────────────────────────────────────────────
def draw_stage_clear(surface: pygame.Surface, stage: int, t: float):
    """Animated 'STAGE X CLEAR!' banner shown briefly between stages."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha   = min(200, int(200 * min(1.0, t / 0.3)))
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))

    cx, cy  = WIDTH // 2, HEIGHT // 2
    bob     = math.sin(t * 6) * 5
    scale   = min(1.0, t / 0.25)

    draw_text_glow(surface, f"STAGE  {stage}  CLEAR!", 60,
                   GOLD, GOLD_DIM, cx, int(cy - 30 + bob),
                   anchor="center", glow_radius=6)
    draw_text_glow(surface, "GET  READY...", 28,
                   CYAN, CYAN_DIM, cx, int(cy + 44 + bob),
                   anchor="center", glow_radius=4)

    # Gold stars bursting from corners
    for sx, sy in [(120, 180), (WIDTH - 120, 180),
                   (120, HEIGHT - 180), (WIDTH - 120, HEIGHT - 180)]:
        draw_star(surface, GOLD, sx, sy, 18, 8, points=5,
                  angle_offset=t * 2.5)


# ─── Menu screen ──────────────────────────────────────────────────────────────
def draw_menu(surface: pygame.Surface, starfield: Starfield,
              balloons: BalloonLayer, t: float):
    surface.fill(SPACE_DARK)
    starfield.draw(surface)
    balloons.draw(surface)

    cx, cy = WIDTH // 2, HEIGHT // 2

    box_w, box_h = 720, 340
    br   = pygame.Rect(cx - box_w // 2, cy - box_h // 2 - 20, box_w, box_h)
    pan  = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    pan.fill((15, 8, 50, 195))
    surface.blit(pan, br)
    pygame.draw.rect(surface, GOLD, br, 3)

    for sx, sy in [(br.left + 14, br.top + 14), (br.right - 14, br.top + 14),
                   (br.left + 14, br.bottom - 14), (br.right - 14, br.bottom - 14)]:
        draw_star(surface, GOLD, sx, sy, 12, 6, points=5, angle_offset=t * 1.8)

    # Aisha Avatar Badge
    import os
    av_path = os.path.join(os.path.dirname(__file__), "assets", "aisha_head.png")
    if os.path.exists(av_path):
        try:
            av = pygame.image.load(av_path).convert_alpha()
            av_scaled = pygame.transform.smoothscale(av, (52, 56))
            surface.blit(av_scaled, av_scaled.get_rect(center=(cx, cy - 135)))
            pygame.draw.circle(surface, GOLD, (cx, cy - 135), 30, 2)
        except Exception:
            pass

    draw_text_glow(surface, "AISHA'S", 56, GOLD, GOLD_DIM,
                   cx, cy - 85, anchor="center", glow_radius=7)
    draw_text_glow(surface, "BIRTHDAY BAKE-OFF!", 44, PINK, PINK_DARK,
                   cx, cy - 22, anchor="center", glow_radius=5)
    draw_text(surface, "Catch falling cake pieces — dodge the obstacles!",
              18, OFF_WHITE, cx, cy + 36, anchor="center")

    if int(t * 2.2) % 2 == 0:
        draw_text(surface, "PRESS  SPACE  TO  START", 24, CYAN,
                  cx, cy + 86, anchor="center", shadow=True)

    draw_text(surface, "← → / A D  MOVE     ESC  PAUSE", 16,
              (120, 140, 170), cx, cy + 124, anchor="center")


# ─── Paused overlay ────────────────────────────────────────────────────────────
def draw_paused(surface: pygame.Surface):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 150))
    surface.blit(ov, (0, 0))
    cx, cy = WIDTH // 2, HEIGHT // 2
    draw_text_glow(surface, "—  PAUSED  —", 58, WHITE, (60, 60, 60),
                   cx, cy - 28, anchor="center", glow_radius=4)
    draw_text(surface, "ESC to Resume   •   Q to Quit to Menu",
              22, CYAN, cx, cy + 44, anchor="center")


# ─── Game Over screen ──────────────────────────────────────────────────────────
def draw_game_over(surface: pygame.Surface, starfield: Starfield,
                   score: int, hi_score: int, stage: int, t: float):
    surface.fill(SPACE_DARK)
    starfield.draw(surface)

    cx, cy  = WIDTH // 2, HEIGHT // 2
    shake   = math.sin(t * 20) * max(0, 4 - t * 3)

    bw, bh = 640, 280
    br   = pygame.Rect(cx - bw // 2, cy - bh // 2 - 20, bw, bh)
    pan  = pygame.Surface((bw, bh), pygame.SRCALPHA)
    pan.fill((70, 5, 5, 210))
    surface.blit(pan, br)
    pygame.draw.rect(surface, RED_BRIGHT, br, 3)

    draw_text_glow(surface, "CAKE  DISASTER!", 52,
                   RED_BRIGHT, RED, cx + int(shake), cy - 68,
                   anchor="center", glow_radius=5)
    draw_text(surface, f"Stage Reached: {stage}", 24, GOLD,
              cx, cy - 6, anchor="center")
    draw_text(surface, f"Score: {score:,}", 28, WHITE,
              cx, cy + 30, anchor="center", shadow=True)
    draw_text(surface, f"Hi-Score: {hi_score:,}", 20, GOLD_DIM,
              cx, cy + 66, anchor="center")

    if int(t * 2) % 2 == 0:
        draw_text(surface, "PRESS  SPACE  TO  RETRY", 22, CYAN,
                  cx, cy + 106, anchor="center")


# ─── Win screen ────────────────────────────────────────────────────────────────
def draw_win(surface: pygame.Surface, starfield: Starfield,
             score: int, hi_score: int, t: float):
    surface.fill(SPACE_DARK)
    starfield.draw(surface)

    cx, cy  = WIDTH // 2, HEIGHT // 2
    bob     = math.sin(t * 3) * 7

    bw, bh = 700, 340
    br   = pygame.Rect(cx - bw // 2, cy - bh // 2 - 20, bw, bh)
    pan  = pygame.Surface((bw, bh), pygame.SRCALPHA)
    pan.fill((30, 25, 5, 215))
    surface.blit(pan, br)
    pygame.draw.rect(surface, GOLD, br, 3)

    for i in range(10):
        angle = t * 1.3 + i * math.pi / 5
        sx    = cx + int(350 * math.cos(angle))
        sy    = (cy - 30) + int(140 * math.sin(angle))
        draw_star(surface, GOLD if i % 2 == 0 else PINK,
                  sx, sy, 10, 5, points=5, angle_offset=angle)

    # Aisha Avatar Badge on Win Screen
    av_path = os.path.join(os.path.dirname(__file__), "assets", "aisha_head.png")
    if os.path.exists(av_path):
        try:
            av = pygame.image.load(av_path).convert_alpha()
            av_scaled = pygame.transform.smoothscale(av, (52, 56))
            surface.blit(av_scaled, av_scaled.get_rect(center=(cx, int(cy - 125 + bob))))
            pygame.draw.circle(surface, GOLD, (cx, int(cy - 125 + bob)), 30, 2)
        except Exception:
            pass

    draw_text_glow(surface, "🎂  AISHA'S  BAKE-OFF  CHAMPION!  🎂", 40,
                   GOLD, GOLD_DIM, cx, int(cy - 78 + bob),
                   anchor="center", glow_radius=7)
    draw_text(surface, "Happy Birthday Aisha — All 10 Stages Conquered!", 22, PINK,
              cx, int(cy - 16 + bob), anchor="center")
    draw_text(surface, f"Final Score: {score:,}", 30, WHITE,
              cx, int(cy + 26 + bob), anchor="center", shadow=True)
    draw_text(surface, f"Hi-Score: {hi_score:,}", 20, GOLD_DIM,
              cx, int(cy + 62 + bob), anchor="center")

    if int(t * 2) % 2 == 0:
        draw_text(surface, "PRESS  SPACE  TO  PLAY  AGAIN", 22, CYAN,
                  cx, int(cy + 104 + bob), anchor="center")


# ─── Leaderboard ──────────────────────────────────────────────────────────────
def draw_leaderboard(surface, scores, current, x, y):
    draw_text(surface, "─ TOP SCORES ─", 18, GOLD_DIM, x, y, anchor="center")
    for i, s in enumerate(scores[:5]):
        col = GOLD if s == current else (180, 180, 200)
        pre = "▶ " if s == current else f"{i+1}. "
        draw_text(surface, f"{pre}{s:,}", 16, col,
                  x, y + 24 + i * 22, anchor="center")
