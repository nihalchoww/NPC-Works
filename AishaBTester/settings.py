# settings.py — Constants for Aisha's Birthday Bake-Off (Catcher Edition)

# ─── Screen ───────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 720
FPS           = 60

# ─── Lives ────────────────────────────────────────────────────────────────────
MAX_LIVES          = 3
INVINCIBLE_SECONDS = 1.5    # Grace period after being hit (flashing)

# ─── Stage system ─────────────────────────────────────────────────────────────
TOTAL_STAGES        = 30
ITEMS_PER_STAGE     = 20    # Items to catch to complete a stage (20 * 50 = 1000 pts)
STAGE_DURATION      = 60    # Seconds per stage (1:00 countdown)
BASE_FALL_SPEED     = 190   # px/s at stage 1
FALL_SPEED_INCREMENT = 12   # px/s added each stage
OBSTACLE_CHANCE     = 0.28  # Probability any spawned item is an obstacle
SPAWN_INTERVAL_BASE = 1.15  # Seconds between spawns at stage 1
SPAWN_INTERVAL_MIN  = 0.40  # Floor for spawn interval (stage 30)

# ─── Player ───────────────────────────────────────────────────────────────────
PLAYER_SPEED     = 340   # px/s horizontal
TRAY_WIDTH       = 70    # Catch zone width (centred on player)
TRAY_HEIGHT      = 14    # Catch zone height

# ─── Scoring ──────────────────────────────────────────────────────────────────
SCORE_CAKE_TIER   = 50
SCORE_CANDLE      = 50
SCORE_STRAWBERRY  = 50
SCORE_CHERRY      = 50
SCORE_CANDY       = 50
SCORE_FROSTING    = 50
STAGE_CLEAR_BONUS = 500
WIN_BONUS         = 2000

# ─── Palette ──────────────────────────────────────────────────────────────────
SPACE_DARK      = ( 15,  10,  45)
SPACE_MID       = ( 25,  18,  70)
COCKPIT_BLUE    = ( 55,  70, 130)
COCKPIT_DARK    = ( 30,  38,  80)
COCKPIT_MID     = ( 45,  58, 105)
PANEL_GREY      = ( 70,  75,  95)
BOLT_GREY       = (100, 108, 130)

CYAN            = (  0, 220, 255)
CYAN_DIM        = (  0,  90, 120)
PINK            = (255, 110, 190)
PINK_LIGHT      = (255, 185, 215)
PINK_DARK       = (180,  50, 120)
GOLD            = (255, 215,   0)
GOLD_DIM        = (160, 135,   0)
RED             = (220,  45,  45)
RED_BRIGHT      = (255,  70,  70)
ORANGE          = (255, 145,   0)
WHITE           = (255, 255, 255)
OFF_WHITE       = (240, 235, 220)
CREAM           = (255, 245, 200)
BROWN_DARK      = ( 55,  28,   8)
BROWN_MID       = (120,  70,  25)
GREEN           = ( 55, 190,  70)
GREEN_DARK      = ( 28, 110,  38)
GREEN_SOUR      = ( 90, 210,  50)
PURPLE          = (160,  60, 230)
BLUE_BRIGHT     = ( 90, 150, 255)
GALAXY_PURPLE   = ( 80,  30, 140)
GALAXY_PINK     = (180,  60, 140)

BALLOON_COLORS  = [PINK, CYAN, GOLD, PURPLE, GREEN, ORANGE, RED_BRIGHT, BLUE_BRIGHT]
BUNTING_COLORS  = [RED_BRIGHT, GOLD, CYAN, PINK, GREEN, PURPLE, ORANGE, PINK_LIGHT]
CONFETTI_COLORS = [RED_BRIGHT, GOLD, CYAN, PINK, GREEN, ORANGE, PURPLE, BLUE_BRIGHT, WHITE]
