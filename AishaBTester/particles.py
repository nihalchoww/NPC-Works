# particles.py — Particle system for Aisha's Birthday Bake-Off (Catcher)
#
# Types:
#   ConfettiParticle  — constant colourful confetti rain (background decor)
#   ScorePopup        — floating +NNN text on catch
#   CollectBurst      — ring of stars on catch
#   FireworkParticle  — burst sparks on WIN screen
#   StageClearBurst   — big burst on stage clear

import math, random
import pygame
from settings import CONFETTI_COLORS, GOLD, GOLD_DIM, CYAN, PINK, ORANGE
from utils import draw_star, get_font, alpha_surface


# ─── Base ──────────────────────────────────────────────────────────────────────
class _Particle:
    def __init__(self, x, y, vx, vy, lifetime, color, size):
        self.x, self.y    = float(x), float(y)
        self.vx, self.vy  = float(vx), float(vy)
        self.lifetime     = lifetime
        self.age          = 0.0
        self.color        = color
        self.size         = size

    @property
    def alive(self): return self.age < self.lifetime

    @property
    def t(self): return min(self.age / max(self.lifetime, 1e-6), 1.0)

    def update(self, dt):
        self.age += dt
        self.x   += self.vx * dt * 60
        self.y   += self.vy * dt * 60


# ─── Confetti ──────────────────────────────────────────────────────────────────
class ConfettiParticle(_Particle):
    """Continuously falling rectangular confetti piece."""

    def __init__(self):
        from settings import WIDTH, HEIGHT
        x   = random.randint(0, WIDTH)
        y   = random.randint(-HEIGHT, 0)    # start above screen
        vx  = random.uniform(-0.5, 0.5)
        vy  = random.uniform(0.8, 2.2)
        lt  = random.uniform(5.0, 14.0)
        col = random.choice(CONFETTI_COLORS)
        sz  = random.randint(4, 9)
        super().__init__(x, y, vx, vy, lt, col, sz)
        self.angle     = random.uniform(0, 360)
        self.spin      = random.uniform(-4, 4)
        self.w         = sz
        self.h         = random.randint(3, 6)

    def update(self, dt):
        super().update(dt)
        self.angle = (self.angle + self.spin) % 360
        from settings import WIDTH, HEIGHT
        if self.y > HEIGHT + 20:
            # Recycle from top
            self.x   = random.randint(0, WIDTH)
            self.y   = -10
            self.age = 0.0

    def draw(self, surface):
        tmp = alpha_surface(self.w + 2, self.h + 2)
        pygame.draw.rect(tmp, self.color, (0, 0, self.w, self.h))
        rot = pygame.transform.rotate(tmp, self.angle)
        surface.blit(rot, rot.get_rect(center=(int(self.x), int(self.y))))


# ─── Score popup ───────────────────────────────────────────────────────────────
class ScorePopup(_Particle):
    def __init__(self, x, y, value):
        label = f"+{value}"
        super().__init__(x, y, 0.0, -0.55, 1.3, GOLD, 24)
        self.label = label

    def draw(self, surface):
        alpha = max(0, int(255 * (1.0 - self.t ** 1.5)))
        font  = get_font(int(self.size))
        img   = font.render(self.label, False, self.color)
        tmp   = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        tmp.blit(img, (0, 0))
        tmp.set_alpha(alpha)
        surface.blit(tmp, tmp.get_rect(center=(int(self.x), int(self.y))))


# ─── Collect burst ─────────────────────────────────────────────────────────────
class CollectBurst:
    def __init__(self, x, y, color):
        self.parts = []
        for i in range(12):
            angle = 2 * math.pi * i / 12
            sp    = random.uniform(1.8, 4.0)
            lt    = random.uniform(0.3, 0.6)
            sz    = random.uniform(4.0, 8.0)
            p     = _Particle(x, y, math.cos(angle)*sp, math.sin(angle)*sp, lt, color, sz)
            self.parts.append(p)

    @property
    def alive(self): return any(p.alive for p in self.parts)

    def update(self, dt):
        for p in self.parts: p.update(dt)

    def draw(self, surface):
        for p in self.parts:
            if p.alive:
                s   = max(1, int(p.size * (1 - p.t * 0.6)))
                a   = max(0.0, 1.0 - p.t)
                col = tuple(int(c * a) for c in p.color)
                if any(c > 0 for c in col):
                    draw_star(surface, col, int(p.x), int(p.y), s, s//2)


# ─── Firework ──────────────────────────────────────────────────────────────────
class FireworkParticle(_Particle):
    def __init__(self, x, y, color):
        angle = random.uniform(0, 2 * math.pi)
        sp    = random.uniform(2.5, 7.0)
        super().__init__(x, y, math.cos(angle)*sp, math.sin(angle)*sp,
                         random.uniform(0.7, 1.5), color, random.uniform(3, 6))
        self.grav = 0.05

    def update(self, dt):
        super().update(dt)
        self.vy += self.grav * dt * 60

    def draw(self, surface):
        a   = max(0.0, 1.0 - self.t)
        col = tuple(int(c * a) for c in self.color)
        s   = max(1, int(self.size * a))
        if any(c > 0 for c in col):
            pygame.draw.circle(surface, col, (int(self.x), int(self.y)), s)


# ─── Stage-clear ring ──────────────────────────────────────────────────────────
class StageClearBurst:
    """Large ring of stars exploding from screen centre on stage clear."""

    def __init__(self, cx, cy):
        self.parts = []
        colors = [GOLD, CYAN, PINK, ORANGE, (255, 255, 255)]
        for i in range(32):
            angle = 2 * math.pi * i / 32
            sp    = random.uniform(3.0, 8.0)
            lt    = random.uniform(0.6, 1.2)
            sz    = random.uniform(5.0, 12.0)
            col   = random.choice(colors)
            p     = _Particle(cx, cy,
                              math.cos(angle)*sp, math.sin(angle)*sp,
                              lt, col, sz)
            self.parts.append(p)

    @property
    def alive(self): return any(p.alive for p in self.parts)

    def update(self, dt):
        for p in self.parts: p.update(dt)

    def draw(self, surface):
        for p in self.parts:
            if p.alive:
                s   = max(1, int(p.size * (1 - p.t * 0.5)))
                a   = max(0.0, 1.0 - p.t)
                col = tuple(int(c * a) for c in p.color)
                if any(c > 0 for c in col):
                    draw_star(surface, col, int(p.x), int(p.y), s, s//2, points=5)


# ─── Particle Manager ──────────────────────────────────────────────────────────
class ParticleManager:
    NUM_CONFETTI = 120

    def __init__(self):
        self._parts  = []
        # Pre-seed confetti (always present during gameplay)
        self._confetti = [ConfettiParticle() for _ in range(self.NUM_CONFETTI)]

    def spawn_score(self, x, y, value):
        self._parts.append(ScorePopup(x, y, value))

    def spawn_collect(self, x, y, color):
        self._parts.append(CollectBurst(x, y, color))

    def spawn_firework(self, x, y, color, count=28):
        for _ in range(count):
            self._parts.append(FireworkParticle(x, y, color))

    def spawn_stage_clear(self, cx, cy):
        self._parts.append(StageClearBurst(cx, cy))

    def update(self, dt, confetti=True):
        if confetti:
            for c in self._confetti:
                c.update(dt)
        self._parts = [p for p in self._parts if p.alive]
        for p in self._parts:
            p.update(dt)

    def draw(self, surface, confetti=True):
        if confetti:
            for c in self._confetti:
                c.draw(surface)
        for p in self._parts:
            if p.alive:
                p.draw(surface)

    def clear(self):
        self._parts.clear()
