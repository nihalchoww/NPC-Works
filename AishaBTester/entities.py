# entities.py — Falling items for Aisha's Birthday Bake-Off (Catcher)
#
# GOOD items (catch on tray):   CakeTier, Candle, Strawberry, Cherry, Candy, FrostingBag
# BAD  items (dodge with body): Anvil, AngryBroccoli, SpoiledMilk
#
# All items fall from the top of the screen.

import math, random
import pygame
from settings import (
    WIDTH, HEIGHT,
    SCORE_CAKE_TIER, SCORE_CANDLE, SCORE_STRAWBERRY,
    SCORE_CHERRY, SCORE_CANDY, SCORE_FROSTING,
    CYAN, PINK, PINK_LIGHT, PINK_DARK, WHITE, OFF_WHITE, CREAM,
    GOLD, RED, RED_BRIGHT, ORANGE, GREEN, GREEN_DARK, GREEN_SOUR,
    BROWN_DARK, BROWN_MID, PANEL_GREY, BOLT_GREY, BLUE_BRIGHT,
)
from utils import draw_star, alpha_surface


# ─── Spawn helper ──────────────────────────────────────────────────────────────
def _random_x(margin=60):
    return random.randint(margin, WIDTH - margin)


# ─── Base falling item ─────────────────────────────────────────────────────────
class _FallingItem:
    RADIUS   = 22   # rough collision half-width
    IS_BAD   = False
    POINTS   = 0
    COLOR    = WHITE
    LABEL    = "?"

    def __init__(self, fall_speed: float):
        self.x          = float(_random_x())
        self.y          = -40.0
        self.vy         = fall_speed
        self.alive      = True
        self._spin      = random.uniform(-1.5, 1.5)   # wobble angle per frame
        self._angle     = 0.0
        self._age       = 0.0

    def update(self, dt: float):
        self._age += dt
        self._angle = (self._angle + self._spin) % 360
        self.y += self.vy * dt
        if self.y > HEIGHT + 80:
            self.alive = False   # missed (fell off bottom)

    def get_rect(self) -> pygame.Rect:
        r = self.RADIUS
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def catch(self):
        self.alive = False

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        raise NotImplementedError


# ════════════════════════════════════════════════════════════════════════════════
#   GOOD ITEMS
# ════════════════════════════════════════════════════════════════════════════════

class CakeTier(_FallingItem):
    """A single tier of birthday cake (3 colours cycling through stages)."""
    RADIUS = 28
    POINTS = SCORE_CAKE_TIER
    COLOR  = PINK
    LABEL  = "Cake Tier"

    _TIER_COLS = [PINK, WHITE, (180, 100, 220), PINK_LIGHT, (255, 160, 80)]

    def __init__(self, fall_speed):
        super().__init__(fall_speed)
        self._col  = random.choice(self._TIER_COLS)
        self._spin = random.uniform(-0.6, 0.6)   # gentle wobble only
        # Size varies slightly
        self.w = random.randint(48, 62)
        self.h = random.randint(20, 28)

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy
        wobble = int(math.sin(self._age * 3) * 4)

        # Main tier body
        pygame.draw.rect(surface, self._col,
                         (cx - self.w//2, cy - self.h//2 + wobble, self.w, self.h))
        # Frosting top
        pygame.draw.rect(surface, WHITE,
                         (cx - self.w//2, cy - self.h//2 - 4 + wobble, self.w, 7))
        # Sprinkles
        for sx, sy, sc in [(-12, 2, CYAN), (0, -2, RED_BRIGHT),
                            (10, 4, GOLD), (-6, 6, PINK)]:
            pygame.draw.rect(surface, sc,
                             (cx + sx, cy + sy + wobble, 5, 2))
        # Border
        pygame.draw.rect(surface, PINK_DARK,
                         (cx - self.w//2, cy - self.h//2 + wobble, self.w, self.h), 2)


class Candle(_FallingItem):
    """A lit birthday candle."""
    RADIUS = 12
    POINTS = SCORE_CANDLE
    COLOR  = GOLD
    LABEL  = "Candle"

    _COLORS = [CYAN, GOLD, PINK, ORANGE, GREEN]

    def __init__(self, fall_speed):
        super().__init__(fall_speed)
        self._col    = random.choice(self._COLORS)
        self._fl_t   = random.uniform(0, 2)

    def update(self, dt):
        super().update(dt)
        self._fl_t += dt

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy
        # Body
        pygame.draw.rect(surface, self._col, (cx - 5, cy - 14, 10, 22))
        # Wick
        pygame.draw.line(surface, BROWN_DARK, (cx, cy - 14), (cx, cy - 18), 2)
        # Flame
        fl = int(self._fl_t * 8) % 2
        fc = GOLD if fl == 0 else ORANGE
        pygame.draw.ellipse(surface, fc, (cx - 5, cy - 26, 10, 12))
        pygame.draw.circle(surface, WHITE, (cx, cy - 22), 2)


class Strawberry(_FallingItem):
    RADIUS = 18
    POINTS = SCORE_STRAWBERRY
    COLOR  = RED_BRIGHT
    LABEL  = "Strawberry"

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy
        wobble = int(math.sin(self._age * 4) * 3)
        cy += wobble
        pygame.draw.circle(surface, RED_BRIGHT, (cx - 5, cy - 2), 11)
        pygame.draw.circle(surface, RED_BRIGHT, (cx + 5, cy - 2), 11)
        pygame.draw.polygon(surface, RED_BRIGHT,
                            [(cx - 13, cy + 4), (cx + 13, cy + 4), (cx, cy + 16)])
        for sx, sy in [(-3, 2), (4, 2), (0, 8), (-6, 7), (6, 7)]:
            pygame.draw.circle(surface, WHITE, (cx + sx, cy + sy), 1)
        leaf = [(cx - 2, cy - 12), (cx - 8, cy - 18), (cx, cy - 15),
                (cx, cy - 12), (cx + 8, cy - 18), (cx + 2, cy - 12)]
        pygame.draw.polygon(surface, GREEN, leaf)


class Cherry(_FallingItem):
    RADIUS = 18
    POINTS = SCORE_CHERRY
    COLOR  = RED_BRIGHT
    LABEL  = "Cherry"

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy
        wobble = int(math.sin(self._age * 5) * 3)
        cy += wobble
        pygame.draw.circle(surface, RED_BRIGHT, (cx - 8, cy + 4), 10)
        pygame.draw.circle(surface, RED_BRIGHT, (cx + 8, cy + 4), 10)
        pygame.draw.line(surface, BROWN_MID, (cx - 8, cy - 6), (cx, cy - 18), 2)
        pygame.draw.line(surface, BROWN_MID, (cx + 8, cy - 6), (cx, cy - 18), 2)
        pygame.draw.circle(surface, (255, 160, 160), (cx - 10, cy + 1), 3)
        pygame.draw.circle(surface, (255, 160, 160), (cx + 6,  cy + 1), 3)


class Candy(_FallingItem):
    """Pink candy / ice-cream cone — like the pink cone from the reference."""
    RADIUS = 18
    POINTS = SCORE_CANDY
    COLOR  = PINK
    LABEL  = "Candy"

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy

        # Draw on temp surface and rotate
        tmp = alpha_surface(50, 60)
        tx, ty = 25, 30
        # Cone body
        pts = [(tx, ty + 20), (tx - 16, ty - 12), (tx + 16, ty - 12)]
        pygame.draw.polygon(tmp, PINK, pts)
        # Swirl lines
        pygame.draw.line(tmp, (220, 70, 160),
                         (tx - 10, ty - 6), (tx + 10, ty - 6), 2)
        pygame.draw.line(tmp, (220, 70, 160),
                         (tx - 8, ty + 4), (tx + 8, ty + 4), 2)
        # Top ball / scoop
        pygame.draw.circle(tmp, PINK_LIGHT, (tx, ty - 14), 14)
        pygame.draw.circle(tmp, WHITE, (tx - 4, ty - 17), 4)
        # Wrapper twist at top
        pygame.draw.ellipse(tmp, (180, 50, 120), (tx - 6, ty - 30, 12, 8))

        rot = pygame.transform.rotate(tmp, self._angle * 0.3)
        surface.blit(rot, rot.get_rect(center=(cx, cy)))


class FrostingBag(_FallingItem):
    """Blue piping bag."""
    RADIUS = 18
    POINTS = SCORE_FROSTING
    COLOR  = BLUE_BRIGHT
    LABEL  = "Frosting Bag"

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy

        tmp = alpha_surface(50, 60)
        tx, ty = 25, 35

        pts = [(tx, ty + 18), (tx - 14, ty - 14), (tx + 14, ty - 14)]
        pygame.draw.polygon(tmp, BLUE_BRIGHT, pts)
        pygame.draw.circle(tmp, PINK, (tx, ty - 16), 6)
        pygame.draw.line(tmp, WHITE, (tx - 5, ty - 16), (tx + 5, ty - 16), 2)
        pygame.draw.rect(tmp, PANEL_GREY, (tx - 4, ty + 16, 8, 10))
        draw_star(tmp, WHITE, tx, ty - 2, 6, 3)

        rot = pygame.transform.rotate(tmp, self._angle * 0.4)
        surface.blit(rot, rot.get_rect(center=(cx, cy)))


# ════════════════════════════════════════════════════════════════════════════════
#   BAD ITEMS (obstacles)
# ════════════════════════════════════════════════════════════════════════════════

class Anvil(_FallingItem):
    RADIUS = 28
    IS_BAD = True
    LABEL  = "Anvil"

    def __init__(self, fall_speed):
        super().__init__(fall_speed * 1.15)   # heavier = slightly faster
        self._spin = random.uniform(-1.2, 1.2)

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy

        tmp = alpha_surface(80, 70)
        tx, ty = 40, 40

        pygame.draw.rect(tmp, (70, 70, 80), (tx - 20, ty, 40, 18))
        pygame.draw.polygon(tmp, (70, 70, 80),
                            [(tx - 20, ty + 4), (tx - 34, ty + 11), (tx - 20, ty + 14)])
        pygame.draw.rect(tmp, (85, 85, 95), (tx - 18, ty - 14, 36, 16))
        pygame.draw.ellipse(tmp, (100, 100, 110), (tx - 18, ty - 16, 36, 8))
        pygame.draw.circle(tmp, BOLT_GREY, (tx - 10, ty + 9), 3)
        pygame.draw.circle(tmp, BOLT_GREY, (tx + 10, ty + 9), 3)

        rot = pygame.transform.rotate(tmp, self._angle)
        surface.blit(rot, rot.get_rect(center=(cx, cy)))


class AngryBroccoli(_FallingItem):
    RADIUS = 24
    IS_BAD = True
    LABEL  = "Angry Broccoli"

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy

        tmp = alpha_surface(72, 72)
        tx, ty = 36, 40

        pygame.draw.rect(tmp, GREEN_DARK, (tx - 5, ty + 2, 10, 18))
        for bx, by, br in [(0, -8, 20), (-11, -2, 14), (11, -2, 14),
                           (-5, -18, 11), (5, -18, 11)]:
            pygame.draw.circle(tmp, GREEN, (tx + bx, ty + by), br)
            pygame.draw.circle(tmp, GREEN_DARK, (tx + bx, ty + by), br, 2)
        pygame.draw.rect(tmp, (15, 50, 15), (tx - 12, ty - 10, 8, 5))
        pygame.draw.rect(tmp, (15, 50, 15), (tx +  4, ty - 10, 8, 5))
        pygame.draw.line(tmp, BROWN_DARK, (tx - 14, ty - 15), (tx - 4, ty - 12), 2)
        pygame.draw.line(tmp, BROWN_DARK, (tx + 4,  ty - 15), (tx + 14, ty - 12), 2)
        pygame.draw.lines(tmp, BROWN_DARK, False,
                          [(tx - 8, ty - 2), (tx - 4, ty + 2),
                           (tx, ty - 2), (tx + 4, ty + 2), (tx + 8, ty - 2)], 2)

        rot = pygame.transform.rotate(tmp, self._angle)
        surface.blit(rot, rot.get_rect(center=(cx, cy)))


class SpoiledMilk(_FallingItem):
    RADIUS = 22
    IS_BAD = True
    LABEL  = "Spoiled Milk"

    def __init__(self, fall_speed):
        super().__init__(fall_speed)
        self._bubble_t = 0.0

    def update(self, dt):
        super().update(dt)
        self._bubble_t += dt

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        cx, cy = int(self.x) + ox, int(self.y) + oy

        tmp = alpha_surface(70, 72)
        tx, ty = 35, 40

        pygame.draw.rect(tmp, (245, 245, 240), (tx - 16, ty - 16, 32, 40))
        pygame.draw.polygon(tmp, (225, 225, 220),
                            [(tx - 16, ty - 16), (tx, ty - 26), (tx + 16, ty - 16)])
        pygame.draw.rect(tmp, (190, 220, 190), (tx - 13, ty - 8, 26, 20))
        pygame.draw.rect(tmp, GREEN_SOUR, (tx - 11, ty - 5, 22, 5))
        pygame.draw.rect(tmp, GREEN_SOUR, (tx - 11, ty + 3, 22, 5))
        # Drip
        pygame.draw.circle(tmp, GREEN_SOUR, (tx, ty + 18), 5)
        pygame.draw.rect(tmp, GREEN_SOUR, (tx - 3, ty + 8, 6, 11))

        rot = pygame.transform.rotate(tmp, self._angle * 0.5)
        surface.blit(rot, rot.get_rect(center=(cx, cy)))

        # Bubble trail (simple animated circles)
        if int(self._bubble_t * 5) % 2 == 0:
            for i in range(2):
                bx = cx + random.randint(-16, 16)
                by = cy - 30 - i * 14
                pygame.draw.circle(surface, GREEN_SOUR, (bx, by), 4, 1)


# ─── Item catalogue ────────────────────────────────────────────────────────────
GOOD_ITEMS = [CakeTier, Candle, Strawberry, Cherry, Candy, FrostingBag]
BAD_ITEMS  = [Anvil, AngryBroccoli, SpoiledMilk]


# ─── Item Spawner ──────────────────────────────────────────────────────────────
class ItemSpawner:
    """
    Spawns a mix of good and bad falling items according to current stage.
    Call update() each frame; items holds active items.
    """

    def __init__(self):
        self.items: list[_FallingItem] = []
        self._timer      = 0.6    # first item comes quickly
        self.fall_speed  = 0.0
        self.spawn_interval = 1.4
        self.obstacle_chance = 0.25

    def configure(self, stage: int,
                  base_speed: float, speed_inc: float,
                  base_interval: float, min_interval: float,
                  obs_chance: float):
        """Call when stage changes."""
        self.fall_speed      = base_speed + (stage - 1) * speed_inc
        self.spawn_interval  = max(min_interval,
                                   base_interval - (stage - 1) * 0.10)
        self.obstacle_chance = min(0.45, obs_chance + (stage - 1) * 0.02)
        self.items.clear()
        self._timer = 0.5

    def update(self, dt: float):
        self._timer -= dt
        if self._timer <= 0:
            self._timer = self.spawn_interval
            self._spawn_one()

        for item in self.items:
            item.update(dt)
        self.items = [i for i in self.items if i.alive]

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        for item in self.items:
            item.draw(surface, offset)

    def check_tray_catch(self, tray_rect: pygame.Rect):
        """Return list of GOOD items that overlap the tray."""
        caught, remaining = [], []
        for item in self.items:
            if not item.IS_BAD and item.get_rect().colliderect(tray_rect):
                item.catch()
                caught.append(item)
            else:
                remaining.append(item)
        self.items = remaining
        return caught

    def check_body_hit(self, body_rect: pygame.Rect):
        """Return first BAD item that overlaps body_rect (removes it)."""
        for i, item in enumerate(self.items):
            if item.IS_BAD and item.get_rect().colliderect(body_rect):
                self.items.pop(i)
                return item
        return None

    def pop_missed_good(self):
        """Return list of GOOD items that fell off the bottom and remove them."""
        missed, alive = [], []
        for item in self.items:
            # alive=False means it went off bottom
            if not item.alive and not item.IS_BAD:
                missed.append(item)
            else:
                alive.append(item)
        self.items = alive
        return missed

    def clear(self):
        self.items.clear()

    def _spawn_one(self):
        if random.random() < self.obstacle_chance:
            cls = random.choice(BAD_ITEMS)
        else:
            cls = random.choice(GOOD_ITEMS)
        self.items.append(cls(self.fall_speed))
