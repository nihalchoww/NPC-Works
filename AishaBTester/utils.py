# utils.py — Shared helper utilities

import math
import pygame
from settings import WHITE


def get_font(size: int, bold: bool = True) -> pygame.font.Font:
    try:
        return pygame.font.SysFont("couriernew,courier,monospace", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


def draw_text(surface, text, size, color, x, y,
              anchor="topleft", shadow=False, shadow_color=(0, 0, 0)):
    font = get_font(size)
    img  = font.render(text, False, color)
    rect = img.get_rect()
    setattr(rect, anchor, (x, y))
    if shadow:
        si = font.render(text, False, shadow_color)
        sr = si.get_rect()
        setattr(sr, anchor, (x + 2, y + 2))
        surface.blit(si, sr)
    surface.blit(img, rect)
    return rect


def draw_text_glow(surface, text, size, color, glow_color,
                   x, y, anchor="center", glow_radius=3):
    font  = get_font(size)
    glow  = font.render(text, False, glow_color)
    for dx in range(-glow_radius, glow_radius + 1, glow_radius):
        for dy in range(-glow_radius, glow_radius + 1, glow_radius):
            if dx == 0 and dy == 0:
                continue
            gr = glow.get_rect()
            setattr(gr, anchor, (x + dx, y + dy))
            surface.blit(glow, gr)
    img  = font.render(text, False, color)
    rect = img.get_rect()
    setattr(rect, anchor, (x, y))
    surface.blit(img, rect)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def draw_star(surface, color, cx, cy, r_outer, r_inner, points=5, angle_offset=0.0):
    pts = []
    for i in range(points * 2):
        angle = math.pi / points * i + angle_offset
        r     = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.sin(angle), cy - r * math.cos(angle)))
    if len(pts) >= 3:
        pygame.draw.polygon(surface, color, pts)


def draw_rounded_rect(surface, color, rect, radius=6):
    r = min(radius, rect.width // 2, rect.height // 2)
    pygame.draw.rect(surface, color, rect.inflate(-2 * r, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2 * r))
    for cx, cy in [(rect.left + r, rect.top + r), (rect.right - r, rect.top + r),
                   (rect.left + r, rect.bottom - r), (rect.right - r, rect.bottom - r)]:
        pygame.draw.circle(surface, color, (cx, cy), r)


def alpha_surface(w, h):
    s = pygame.Surface((max(1, w), max(1, h)), pygame.SRCALPHA)
    s.fill((0, 0, 0, 0))
    return s


def color_lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
