# game.py — Main game state machine for Anti-Gravity Birthday Bake-Off (Catcher Edition)
#
# States: MENU → PLAYING → STAGE_CLEAR → PLAYING ... → GAME_OVER | WIN → MENU
#
# Responsibilities:
#   • State transitions & event routing
#   • Coordinating player, item spawner, particles, HUD
#   • Stage progression (1 to 10), lives, timer, scoring
#   • Screen-shake and visual effects
#   • Leaderboard (scores.json, top 5)

import math
import random
import json
import os
import pygame

from settings import (
    WIDTH, HEIGHT, FPS,
    MAX_LIVES, INVINCIBLE_SECONDS,
    TOTAL_STAGES, ITEMS_PER_STAGE, STAGE_DURATION,
    BASE_FALL_SPEED, FALL_SPEED_INCREMENT,
    OBSTACLE_CHANCE, SPAWN_INTERVAL_BASE, SPAWN_INTERVAL_MIN,
    STAGE_CLEAR_BONUS, WIN_BONUS,
    SPACE_DARK, RED_BRIGHT, BALLOON_COLORS,
)
from player import Player
from entities import ItemSpawner
from particles import ParticleManager
from ui import (
    HUD, Starfield, BalloonLayer,
    draw_cockpit_background, draw_bunting,
    draw_menu, draw_paused, draw_stage_clear,
    draw_game_over, draw_win, draw_leaderboard,
)


# ─── Game states ───────────────────────────────────────────────────────────────
STATE_MENU        = "MENU"
STATE_PLAYING     = "PLAYING"
STATE_STAGE_CLEAR = "STAGE_CLEAR"
STATE_PAUSED      = "PAUSED"
STATE_GAME_OVER   = "GAME_OVER"
STATE_WIN         = "WIN"

SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.json")


class Game:
    """
    Top-level game object. Call run() to start the game loop.
    """

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
        self.state  = STATE_MENU

        # Background layers
        self.starfield = Starfield()
        self.balloons  = BalloonLayer(n=12)
        self.hud       = HUD()
        self.particles = ParticleManager()
        self.spawner   = ItemSpawner()

        # Gameplay entities & variables
        self.player              = None
        self.score               = 0
        self.lives               = MAX_LIVES
        self.stage               = 1
        self.items_caught_stage  = 0
        self.time_left           = float(STAGE_DURATION)
        self.shake_timer         = 0.0
        self._stage_clear_timer  = 0.0
        self._fw_timer           = 0.0
        self._t                  = 0.0   # global elapsed time

        # Leaderboard
        self.leaderboard: list[int] = self._load_scores()

    # ─── Leaderboard persistence ──────────────────────────────────────────────

    def _load_scores(self) -> list[int]:
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "r") as f:
                    data = json.load(f)
                    scores = data.get("scores", [])
                    if isinstance(scores, list) and scores:
                        return sorted([int(s) for s in scores], reverse=True)[:5]
            except Exception:
                pass
        return [1000, 500, 250, 100, 50]

    def _save_score(self, new_score: int):
        self.leaderboard.append(new_score)
        self.leaderboard = sorted(self.leaderboard, reverse=True)[:5]
        try:
            with open(SCORES_FILE, "w") as f:
                json.dump({"scores": self.leaderboard}, f, indent=2)
        except Exception:
            pass

    # ─── Game lifecycle ───────────────────────────────────────────────────────

    def _start_game(self):
        self.score              = 0
        self.lives              = MAX_LIVES
        self.stage              = 1
        self.items_caught_stage = 0
        self.shake_timer        = 0.0
        self._stage_clear_timer = 0.0
        self.player             = Player(x=WIDTH // 2, y=HEIGHT - 105)
        self.particles.clear()
        self._start_stage()
        self.state              = STATE_PLAYING

    def _start_stage(self):
        self.items_caught_stage = 0
        self.time_left          = float(STAGE_DURATION)
        self.spawner.configure(
            stage=self.stage,
            base_speed=BASE_FALL_SPEED,
            speed_inc=FALL_SPEED_INCREMENT,
            base_interval=SPAWN_INTERVAL_BASE,
            min_interval=SPAWN_INTERVAL_MIN,
            obs_chance=OBSTACLE_CHANCE,
        )

    def _end_game(self, won: bool):
        if won:
            self.score += WIN_BONUS
            self.state = STATE_WIN
            self._fw_timer = 0.0
        else:
            self.state = STATE_GAME_OVER

        self._save_score(self.score)

    # ─── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        """Start and run the game loop until the user quits."""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)   # cap dt to avoid physics blow-up on lag

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

    # ─── Event handling ────────────────────────────────────────────────────────

    def _handle_event(self, event: pygame.event.Event):
        if self.state == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._start_game()

        elif self.state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED

        elif self.state == STATE_STAGE_CLEAR:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED

        elif self.state == STATE_PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_PLAYING
                elif event.key == pygame.K_q:
                    self.state = STATE_MENU

        elif self.state in (STATE_GAME_OVER, STATE_WIN):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._start_game()

    # ─── Update ────────────────────────────────────────────────────────────────

    def _update(self, dt: float):
        self._t += dt
        self.starfield.update(dt)
        self.balloons.update(dt)
        self.hud.update(dt)
        self.shake_timer = max(0.0, self.shake_timer - dt)

        if self.state == STATE_MENU:
            pass

        elif self.state == STATE_PLAYING:
            self._update_playing(dt)

        elif self.state == STATE_STAGE_CLEAR:
            self._update_stage_clear(dt)

        elif self.state == STATE_WIN:
            self._update_win(dt)

        elif self.state == STATE_GAME_OVER:
            self.particles.update(dt, confetti=False)

    def _update_playing(self, dt: float):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        self.spawner.update(dt)
        self.particles.update(dt, confetti=True)

        # Stage countdown timer
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.lives -= 1
            self.shake_timer = 0.4
            self.player.make_invincible(INVINCIBLE_SECONDS)
            self.particles.spawn_score(self.player.x, self.player.y - 40, "TIME UP!")
            if self.lives <= 0:
                self._end_game(won=False)
                return
            else:
                self.time_left = float(STAGE_DURATION)

        # 1. Tray catch (good items)
        caught_goods = self.spawner.check_tray_catch(self.player.get_tray_rect())
        for item in caught_goods:
            pts = getattr(item, "POINTS", 100)
            col = getattr(item, "COLOR", (255, 215, 0))
            self.score += pts
            self.items_caught_stage += 1
            self.particles.spawn_collect(item.x, item.y, col)
            self.particles.spawn_score(item.x, item.y - 15, f"+{pts}")

        # Check if stage goal achieved
        if self.items_caught_stage >= ITEMS_PER_STAGE:
            self.score += STAGE_CLEAR_BONUS
            self.particles.spawn_stage_clear(WIDTH // 2, HEIGHT // 2)
            self.state = STATE_STAGE_CLEAR
            self._stage_clear_timer = 1.8
            return

        # 2. Body obstacle collisions
        if not self.player.invincible:
            bad_item = self.spawner.check_body_hit(self.player.get_body_rect())
            if bad_item:
                self.lives -= 1
                self.shake_timer = 0.35
                self.player.make_invincible(INVINCIBLE_SECONDS)
                self.particles.spawn_collect(bad_item.x, bad_item.y, RED_BRIGHT)
                self.particles.spawn_score(bad_item.x, bad_item.y - 20, "OUCH!")
                if self.lives <= 0:
                    self._end_game(won=False)
                    return

        # 3. Clean up missed good items
        self.spawner.pop_missed_good()

    def _update_stage_clear(self, dt: float):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        self.particles.update(dt, confetti=True)
        self._stage_clear_timer -= dt

        if self._stage_clear_timer <= 0:
            self.stage += 1
            if self.stage > TOTAL_STAGES:
                self._end_game(won=True)
            else:
                self._start_stage()
                self.state = STATE_PLAYING

    def _update_win(self, dt: float):
        self._fw_timer -= dt
        if self._fw_timer <= 0:
            self._fw_timer = random.uniform(0.18, 0.42)
            cx = random.randint(200, WIDTH - 200)
            cy = random.randint(100, HEIGHT - 250)
            col = random.choice(BALLOON_COLORS)
            self.particles.spawn_firework(cx, cy, col, count=28)
        self.particles.update(dt, confetti=True)

    # ─── Draw ──────────────────────────────────────────────────────────────────

    def _draw(self):
        ox = random.randint(-4, 4) if self.shake_timer > 0 else 0
        oy = random.randint(-4, 4) if self.shake_timer > 0 else 0
        offset = (ox, oy)

        if self.state == STATE_MENU:
            draw_menu(self.screen, self.starfield, self.balloons, self._t)
            draw_leaderboard(self.screen, self.leaderboard, -1, WIDTH // 2, HEIGHT - 180)

        elif self.state in (STATE_PLAYING, STATE_STAGE_CLEAR, STATE_PAUSED):
            draw_cockpit_background(self.screen, self.starfield, self._t, offset=offset)
            self.balloons.draw(self.screen)
            draw_bunting(self.screen, self._t, offset=offset)
            self.spawner.draw(self.screen, offset=offset)
            if self.player:
                self.player.draw(self.screen, offset=offset)
            self.particles.draw(self.screen, confetti=True)

            hi_score = max([self.score] + self.leaderboard) if self.leaderboard else self.score
            self.hud.draw(
                self.screen,
                score=self.score,
                hi_score=hi_score,
                lives=self.lives,
                max_lives=MAX_LIVES,
                time_left=self.time_left,
                stage=self.stage,
                total_stages=TOTAL_STAGES,
            )

            if self.state == STATE_STAGE_CLEAR:
                elapsed = max(0.0, 1.8 - self._stage_clear_timer)
                draw_stage_clear(self.screen, self.stage, elapsed)

            elif self.state == STATE_PAUSED:
                draw_paused(self.screen)

        elif self.state == STATE_GAME_OVER:
            hi_score = max(self.leaderboard) if self.leaderboard else self.score
            draw_game_over(self.screen, self.starfield, self.score, hi_score, self.stage, self._t)
            draw_leaderboard(self.screen, self.leaderboard, self.score, WIDTH // 2, HEIGHT - 170)

        elif self.state == STATE_WIN:
            hi_score = max(self.leaderboard) if self.leaderboard else self.score
            draw_win(self.screen, self.starfield, self.score, hi_score, self._t)
            self.particles.draw(self.screen, confetti=False)
            draw_leaderboard(self.screen, self.leaderboard, self.score, WIDTH // 2, HEIGHT - 160)
