import base64
import os

with open("assets/aisha_web_head.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0a0520">
<title>Aisha's Birthday Bake-Off 🎂</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
    -webkit-user-select: none;
    -webkit-touch-callout: none;
    -webkit-tap-highlight-color: transparent;
  }
  html, body {
    width: 100%;
    height: 100%;
    height: 100dvh;
    overflow: hidden;
    background: #080417;
    color: #fff;
    font-family: 'Press Start 2P', monospace, sans-serif;
    touch-action: none;
  }
  #game-wrap {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at center, #1b1248 0%, #0d0824 60%, #060312 100%);
  }
  canvas {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    touch-action: none;
  }
  /* Subtle Retro CRT Scanline overlay */
  .scanlines {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(rgba(18, 16, 38, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
    background-size: 100% 4px;
    opacity: 0.65;
    z-index: 10;
  }
  /* Mobile Virtual Controls */
  .hud-btn {
    position: absolute;
    z-index: 25;
    background: rgba(15, 25, 60, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 2px solid #00dcff;
    color: #00dcff;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 0 15px rgba(0, 220, 255, 0.3);
    touch-action: manipulation;
  }
  .hud-btn:active {
    background: rgba(0, 220, 255, 0.35);
    transform: scale(0.92);
  }
  #pause-btn {
    top: max(14px, env(safe-area-inset-top));
    right: max(14px, env(safe-area-inset-right));
  }
  #fs-btn {
    top: max(14px, env(safe-area-inset-top));
    left: max(14px, env(safe-area-inset-left));
    font-size: 16px;
  }
  /* Mobile Thumb Controls */
  #touch-controls {
    display: none;
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 20;
  }
  @media (pointer: coarse), (max-width: 900px) {
    #touch-controls { display: block; }
  }

  /* Left & Right moving icons shifted to the left and right middle sides of the screen */
  .thumb-zone {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: auto;
    z-index: 25;
  }
  .zone-left {
    left: max(16px, env(safe-area-inset-left));
  }
  .zone-right {
    right: max(16px, env(safe-area-inset-right));
  }

  .control-btn {
    width: 74px;
    height: 74px;
    border-radius: 50%;
    background: rgba(14, 18, 52, 0.75);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 2.5px solid #00dcff;
    color: #00dcff;
    font-size: 30px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.7), 0 0 16px rgba(0, 220, 255, 0.35), inset 0 0 14px rgba(0, 220, 255, 0.2);
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
    transition: transform 0.08s ease, background 0.08s ease, box-shadow 0.08s ease, border-color 0.08s ease;
  }
  .control-btn:active, .control-btn.active {
    background: rgba(0, 220, 255, 0.45);
    color: #ffffff;
    border-color: #ffffff;
    transform: scale(0.90);
    box-shadow: 0 0 28px rgba(0, 220, 255, 0.9), inset 0 0 16px #ffffff;
  }

  /* Action button (START / RETRY) at bottom center for menus */
  .action-zone {
    position: absolute;
    bottom: max(18px, env(safe-area-inset-bottom));
    left: 50%;
    transform: translateX(-50%);
    pointer-events: auto;
    z-index: 22;
  }
  .btn-action {
    width: auto;
    min-width: 140px;
    height: 48px;
    padding: 0 24px;
    border-radius: 24px;
    font-size: 12px;
    letter-spacing: 1.5px;
    border-color: #ffd700;
    color: #ffd700;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6), 0 0 16px rgba(255, 215, 0, 0.4), inset 0 0 10px rgba(255, 215, 0, 0.25);
  }
  .btn-action:active, .btn-action.active {
    background: rgba(255, 215, 0, 0.4);
    box-shadow: 0 0 26px rgba(255, 215, 0, 0.85), inset 0 0 14px #ffffff;
    color: #ffffff;
  }
</style>
</head>
<body>

<div id="game-wrap">
  <div class="scanlines"></div>
  <canvas id="gameCanvas"></canvas>
  <button class="hud-btn" id="fs-btn" title="Toggle Fullscreen">⛶</button>
  <button class="hud-btn" id="pause-btn" title="Pause / Resume">⏸</button>
  <div id="touch-controls">
    <div class="thumb-zone zone-left">
      <button class="control-btn" id="btn-left" aria-label="Move Left">◀</button>
    </div>
    <div class="thumb-zone zone-right">
      <button class="control-btn" id="btn-right" aria-label="Move Right">▶</button>
    </div>
    <div class="action-zone" id="action-zone">
      <button class="control-btn btn-action" id="btn-action">START</button>
    </div>
  </div>
</div>

<script>
(() => {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Load Aisha Portrait & Head Sprites
  const aishaPortrait = new Image();
  aishaPortrait.src = "data:image/jpeg;base64,%%AISHA_PORTRAIT_B64%%";

  const aishaHead = new Image();
  aishaHead.src = "data:image/png;base64,%%AISHA_HEAD_B64%%";

  // Web Audio Synthesizer (Retro 16-bit arcade sound chip)
  let audioCtx = null;
  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }
  ['touchstart', 'pointerdown', 'click', 'keydown'].forEach(ev => {
    window.addEventListener(ev, initAudio, { passive: true, once: false });
  });

  function playTone(freq, type, duration, gainVal=0.15) {
    if (!audioCtx || audioCtx.state !== 'running') return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch(e) {}
  }
  function sfxCatch() {
    initAudio();
    playTone(523, 'triangle', 0.08, 0.18); // C5
    setTimeout(() => playTone(659, 'triangle', 0.09, 0.18), 40); // E5
    setTimeout(() => playTone(784, 'triangle', 0.12, 0.18), 80); // G5
  }
  function sfxHit() {
    initAudio();
    playTone(140, 'sawtooth', 0.22, 0.3);
    setTimeout(() => playTone(95, 'sawtooth', 0.2, 0.25), 60);
  }
  function sfxWin() {
    initAudio();
    const melody = [523, 659, 784, 1046];
    melody.forEach((f, i) => {
      setTimeout(() => playTone(f, 'square', 0.14, 0.16), i * 110);
    });
  }

  // Haptic feedback
  function haptic(ms) {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try { navigator.vibrate(ms); } catch(e) {}
    }
  }

  // Dynamic Viewport
  let WIDTH = 720;
  let HEIGHT = 1280;

  function handleResize() {
    const isPortrait = window.innerHeight > window.innerWidth;
    if (isPortrait) {
      WIDTH = 720;
      const ratio = window.innerHeight / window.innerWidth;
      HEIGHT = Math.round(720 * ratio);
      HEIGHT = Math.max(1080, Math.min(1600, HEIGHT));
    } else {
      HEIGHT = 720;
      const ratio = window.innerWidth / window.innerHeight;
      WIDTH = Math.round(720 * ratio);
      WIDTH = Math.max(1080, Math.min(1600, WIDTH));
    }
    canvas.width = WIDTH;
    canvas.height = HEIGHT;
    player.y = HEIGHT - 115;
    player.x = Math.max(player.w / 2, Math.min(WIDTH - player.w / 2, player.x));
  }
  window.addEventListener('resize', handleResize);
  window.addEventListener('orientationchange', () => setTimeout(handleResize, 200));

  // Game Constants
  const TOTAL_STAGES = 10;
  const ITEMS_PER_STAGE = 10;
  const STAGE_DURATION = 38;
  const MAX_LIVES = 3;

  const COLORS = {
    SPACE_DARK: '#0b0621',
    SPACE_MID: '#1b1248',
    COCKPIT_BLUE: '#374682',
    COCKPIT_DARK: '#161c3c',
    COCKPIT_MID: '#283363',
    CYAN: '#00dcff',
    CYAN_GLOW: '#00f0ff',
    PINK: '#ff6ebe',
    GOLD: '#ffd700',
    RED: '#ff4646',
    WHITE: '#ffffff',
    ORANGE: '#ff9100',
    GREEN: '#37be46',
    PURPLE: '#a03ce6'
  };

  // State
  let state = 'MENU';
  let score = 0;
  let hiScore = parseInt(localStorage.getItem('anti_grav_hiscore') || '1000');
  let lives = MAX_LIVES;
  let stage = 1;
  let itemsCaughtStage = 0;
  let timeLeft = STAGE_DURATION;
  let shakeTime = 0;
  let stageClearTime = 0;
  let globalTime = 0;

  // Player
  const player = {
    x: 360,
    y: 1165,
    w: 60,
    h: 110,
    speed: 520,
    invincible: 0,
    walkTime: 0
  };

  // Touch Dragging Mechanics
  let isDragging = false;
  let targetX = player.x;

  function getCanvasCoords(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  window.addEventListener('pointerdown', (e) => {
    initAudio();
    if (e.target.closest('.hud-btn') || e.target.closest('#touch-controls')) return;
    if (state === 'MENU' || state === 'GAME_OVER' || state === 'WIN') {
      startGame();
      haptic(25);
      return;
    }
    if (state === 'PAUSED') {
      state = 'PLAYING';
      return;
    }
    isDragging = true;
    targetX = getCanvasCoords(e.clientX, e.clientY).x;
  }, { passive: true });

  window.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    targetX = getCanvasCoords(e.clientX, e.clientY).x;
  }, { passive: true });

  window.addEventListener('pointerup', () => { isDragging = false; });
  window.addEventListener('pointercancel', () => { isDragging = false; });

  // Keyboard controls
  const keys = {};
  window.addEventListener('keydown', (e) => {
    initAudio();
    keys[e.code] = true;
    if (e.code === 'Space') {
      if (state === 'MENU' || state === 'GAME_OVER' || state === 'WIN') startGame();
    }
    if (e.code === 'Escape') {
      state = (state === 'PLAYING') ? 'PAUSED' : (state === 'PAUSED' ? 'PLAYING' : state);
    }
    if (e.code === 'KeyQ' && state === 'PAUSED') state = 'MENU';
  });
  window.addEventListener('keyup', (e) => { keys[e.code] = false; });

  // Touch Buttons
  const btnL = document.getElementById('btn-left');
  const btnR = document.getElementById('btn-right');
  const btnAction = document.getElementById('btn-action');
  const actionZone = document.getElementById('action-zone');
  const btnPause = document.getElementById('pause-btn');
  const btnFS = document.getElementById('fs-btn');

  function syncUIState() {
    if (actionZone) {
      actionZone.style.display = (state === 'PLAYING') ? 'none' : 'block';
    }
  }

  function bindBtn(elem, code) {
    elem.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      keys[code] = true;
      elem.classList.add('active');
      haptic(15);
    });
    const release = (e) => {
      e.preventDefault();
      keys[code] = false;
      elem.classList.remove('active');
    };
    elem.addEventListener('pointerup', release);
    elem.addEventListener('pointercancel', release);
    elem.addEventListener('pointerleave', release);
  }
  bindBtn(btnL, 'ArrowLeft');
  bindBtn(btnR, 'ArrowRight');

  btnAction.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    e.stopPropagation();
    initAudio();
    haptic(25);
    if (state === 'MENU' || state === 'GAME_OVER' || state === 'WIN') startGame();
    else if (state === 'PLAYING') state = 'PAUSED';
    else if (state === 'PAUSED') state = 'PLAYING';
    syncUIState();
  });

  btnPause.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    initAudio();
    haptic(20);
    if (state === 'PLAYING') state = 'PAUSED';
    else if (state === 'PAUSED') state = 'PLAYING';
    syncUIState();
  });

  btnFS.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  // Twinkling Pixel Stars with 4-point sparkle
  const stars = [];
  for (let i = 0; i < 140; i++) {
    stars.push({
      x: Math.random() * 1400,
      y: Math.random() * 1600,
      size: Math.random() < 0.6 ? 2 : (Math.random() < 0.85 ? 3 : 4),
      speed: 0.15 + Math.random() * 0.45,
      twinkle: Math.random() * Math.PI * 2,
      color: Math.random() < 0.7 ? '#ffffff' : (Math.random() < 0.5 ? '#00dcff' : '#ffb3d9')
    });
  }

  // Drifting Helium Balloons
  const bColors = [COLORS.PINK, COLORS.CYAN, COLORS.GOLD, COLORS.PURPLE, COLORS.GREEN, COLORS.ORANGE];
  const balloons = [];
  for (let i = 0; i < 12; i++) {
    balloons.push({
      x: Math.random() * 1400,
      y: Math.random() * 1600,
      sz: 16 + Math.random() * 10,
      dy: -0.4 - Math.random() * 0.45,
      color: bColors[Math.floor(Math.random() * bColors.length)],
      phase: Math.random() * Math.PI * 2
    });
  }

  // Retro Confetti
  const confetti = [];
  for (let i = 0; i < 65; i++) {
    confetti.push({
      x: Math.random() * 1400,
      y: Math.random() * 1600,
      vy: 45 + Math.random() * 65,
      color: bColors[Math.floor(Math.random() * bColors.length)],
      sz: 3 + Math.random() * 3,
      rot: Math.random() * 6
    });
  }

  // Stardust trail particles behind falling items
  let trails = [];

  // Item Catalogue
  const GOOD_KINDS = ['CAKE', 'STRAWBERRY', 'CHERRY', 'CANDLE', 'CANDY', 'FROSTING'];
  const BAD_KINDS = ['ANVIL', 'BROCCOLI', 'SPOILED_MILK'];

  const GOOD_POINTS = {
    CAKE: 200,
    STRAWBERRY: 150,
    CHERRY: 180,
    CANDLE: 100,
    CANDY: 120,
    FROSTING: 220
  };

  // Particles
  let particles = [];
  function addCollectBurst(x, y, color) {
    for (let i = 0; i < 18; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 70 + Math.random() * 160;
      particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.45,
        maxLife: 0.45,
        color: color,
        size: 3 + Math.random() * 3
      });
    }
  }

  function addScorePopup(x, y, text, color=COLORS.GOLD) {
    particles.push({
      x, y,
      vx: 0,
      vy: -55,
      life: 0.85,
      maxLife: 0.85,
      text: text,
      color: color,
      isText: true
    });
  }

  function addFireworks(x, y, color) {
    for (let i = 0; i < 30; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 90 + Math.random() * 210;
      particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.8,
        maxLife: 0.8,
        color: color,
        size: 4
      });
    }
  }

  // Items
  let items = [];
  let spawnTimer = 0.5;

  function startGame() {
    score = 0;
    lives = MAX_LIVES;
    stage = 1;
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    shakeTime = 0;
    items = [];
    particles = [];
    trails = [];
    player.x = WIDTH / 2;
    player.invincible = 0;
    targetX = player.x;
    state = 'PLAYING';
    btnAction.textContent = 'PAUSE';
    syncUIState();
  }

  function nextStage() {
    stage++;
    if (stage > TOTAL_STAGES) {
      score += 2000;
      if (score > hiScore) {
        hiScore = score;
        localStorage.setItem('anti_grav_hiscore', hiScore);
      }
      state = 'WIN';
      btnAction.textContent = 'AGAIN';
      sfxWin();
      haptic([40, 50, 40, 50, 100]);
      syncUIState();
    } else {
      itemsCaughtStage = 0;
      timeLeft = STAGE_DURATION;
      items = [];
      state = 'PLAYING';
      syncUIState();
    }
  }

  function endGame() {
    if (score > hiScore) {
      hiScore = score;
      localStorage.setItem('anti_grav_hiscore', hiScore);
    }
    state = 'GAME_OVER';
    btnAction.textContent = 'RETRY';
    haptic([100, 80, 120]);
    syncUIState();
  }

  // ─── 16-BIT RETRO PIXEL SPRITE RENDERERS ──────────────────────────────

  function drawAishaPortrait(ctx, x, y, width, height, floatY) {
    const py = y + (floatY || 0);
    const radius = 14;

    // Glowing drop shadow & bezel
    ctx.save();
    ctx.shadowColor = 'rgba(255, 77, 166, 0.65)';
    ctx.shadowBlur = 24;
    ctx.fillStyle = '#0a0620';
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x - width / 2, py - height / 2, width, height, radius);
    else ctx.rect(x - width / 2, py - height / 2, width, height);
    ctx.fill();

    // Gold arcade border
    ctx.strokeStyle = COLORS.GOLD;
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.restore();

    // Clip & draw Aisha's actual photo
    if (aishaPortrait.complete && aishaPortrait.naturalWidth > 0) {
      ctx.save();
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(x - width / 2, py - height / 2, width, height, radius);
      else ctx.rect(x - width / 2, py - height / 2, width, height);
      ctx.clip();
      ctx.drawImage(aishaPortrait, x - width / 2, py - height / 2, width, height);
      ctx.restore();
    }

    // Inner cyan neon rim
    ctx.strokeStyle = COLORS.CYAN;
    ctx.lineWidth = 2;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x - width / 2 + 3, py - height / 2 + 3, width - 6, height - 6, radius - 2);
    else ctx.rect(x - width / 2 + 3, py - height / 2 + 3, width - 6, height - 6);
    ctx.stroke();

    // 4 Corner Gold Gems
    const corners = [
      [x - width / 2 + 8, py - height / 2 + 8],
      [x + width / 2 - 16, py - height / 2 + 8],
      [x - width / 2 + 8, py + height / 2 - 16],
      [x + width / 2 - 16, py + height / 2 - 16]
    ];
    corners.forEach(([cx, cy]) => {
      ctx.fillStyle = COLORS.GOLD;
      ctx.fillRect(cx, cy, 8, 8);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(cx + 2, cy + 2, 4, 4);
    });

    // Orbiting Sparkles around portrait corners
    const t = globalTime * 3;
    for (let i = 0; i < 4; i++) {
      const angle = t + (i * Math.PI / 2);
      const orbitR = 12;
      const [cx, cy] = corners[i];
      const sx = cx + 4 + Math.cos(angle) * orbitR;
      const sy = cy + 4 + Math.sin(angle) * orbitR;
      ctx.fillStyle = (i % 2 === 0) ? COLORS.GOLD : COLORS.PINK;
      ctx.fillRect(sx - 2, sy - 2, 4, 4);
    }
  }

  function drawCake(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Triangular cake wedge slice (matching mockup)
    ctx.fillStyle = '#f4a261';
    ctx.beginPath();
    ctx.moveTo(-16, 12); ctx.lineTo(16, 12); ctx.lineTo(12, -4); ctx.lineTo(-12, -4);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#fff3b0';
    ctx.fillRect(-14, 2, 28, 4);
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(-13, -4); ctx.lineTo(13, -4); ctx.lineTo(8, -14); ctx.lineTo(-8, -14);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#ff4d6d';
    ctx.fillRect(-10, -8, 20, 4);
    ctx.fillStyle = '#c9184a';
    ctx.beginPath(); ctx.arc(0, -17, 5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffffff'; ctx.fillRect(-2, -19, 2, 2);
    ctx.restore();
  }

  function drawStrawberry(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Plump ruby berry
    ctx.fillStyle = '#e61842';
    ctx.beginPath();
    ctx.moveTo(0, 16);
    ctx.bezierCurveTo(-16, 4, -16, -10, 0, -8);
    ctx.bezierCurveTo(16, -10, 16, 4, 0, 16);
    ctx.fill();
    // Shading highlight
    ctx.fillStyle = '#ff758f';
    ctx.beginPath(); ctx.arc(-4, -1, 5, 0, Math.PI * 2); ctx.fill();
    // Seed specks
    ctx.fillStyle = '#ffea00';
    [[-6, -3], [0, -5], [5, -3], [-8, 2], [-2, 1], [4, 2], [-3, 8], [2, 8], [0, 12]].forEach(([sx, sy]) => {
      ctx.fillRect(sx, sy, 2, 2);
    });
    // Leaf crown
    ctx.fillStyle = '#2ec4b6';
    ctx.beginPath();
    ctx.moveTo(0, -9);
    ctx.lineTo(-8, -15); ctx.lineTo(-3, -10);
    ctx.lineTo(0, -17);
    ctx.lineTo(3, -10); ctx.lineTo(8, -15);
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle = '#1b7a6f';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0, -10); ctx.quadraticCurveTo(2, -20, 6, -18); ctx.stroke();
    ctx.restore();
  }

  function drawCherry(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Twin Stems
    ctx.strokeStyle = '#40916c';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(-7, 2); ctx.quadraticCurveTo(-4, -16, 2, -18);
    ctx.moveTo(7, 6); ctx.quadraticCurveTo(5, -12, 2, -18);
    ctx.stroke();
    // Green Leaf
    ctx.fillStyle = '#2d6a4f';
    ctx.beginPath();
    ctx.ellipse(6, -16, 6, 3, Math.PI / 4, 0, Math.PI * 2); ctx.fill();
    // Cherries
    ctx.fillStyle = '#ba181b';
    ctx.beginPath(); ctx.arc(-8, 5, 8, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ff758f';
    ctx.beginPath(); ctx.arc(-10, 3, 3, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = '#9b111e';
    ctx.beginPath(); ctx.arc(7, 8, 8, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ff758f';
    ctx.beginPath(); ctx.arc(5, 6, 3, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  function drawCandle(ctx, x, y, rot, fl_t) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Candle body
    ctx.fillStyle = '#00dcff';
    ctx.fillRect(-5, -6, 10, 22);
    // White spiral wax stripes
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-5, -2, 10, 3);
    ctx.fillRect(-5, 6, 10, 3);
    ctx.fillRect(-5, 14, 10, 3);
    // Wick
    ctx.strokeStyle = '#222';
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0, -6); ctx.lineTo(0, -11); ctx.stroke();
    // Animated glowing flame
    const flick = Math.sin(fl_t * 14) * 2;
    ctx.fillStyle = 'rgba(255, 165, 0, 0.45)';
    ctx.beginPath(); ctx.arc(0, -18, 9 + flick * 0.5, 0, Math.PI * 2); ctx.fill();
    // Outer flame
    ctx.fillStyle = '#ff7b00';
    ctx.beginPath();
    ctx.moveTo(0, -24 + flick);
    ctx.quadraticCurveTo(-6, -17, 0, -11);
    ctx.quadraticCurveTo(6, -17, 0, -24 + flick);
    ctx.fill();
    // Inner flame
    ctx.fillStyle = '#ffe600';
    ctx.beginPath();
    ctx.moveTo(0, -21 + flick * 0.7);
    ctx.quadraticCurveTo(-3, -16, 0, -12);
    ctx.quadraticCurveTo(3, -16, 0, -21 + flick * 0.7);
    ctx.fill();
    ctx.fillStyle = '#ffffff'; ctx.fillRect(-1, -15, 2, 3);
    ctx.restore();
  }

  function drawCandy(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Wrapper ends
    ctx.fillStyle = '#ff6ebe';
    ctx.beginPath();
    ctx.moveTo(-11, 0); ctx.lineTo(-20, -9); ctx.lineTo(-18, 0); ctx.lineTo(-20, 9); ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(11, 0); ctx.lineTo(20, -9); ctx.lineTo(18, 0); ctx.lineTo(20, 9); ctx.closePath();
    ctx.fill();
    // Candy ball
    ctx.fillStyle = '#ff2a85';
    ctx.beginPath(); ctx.arc(0, 0, 11, 0, Math.PI * 2); ctx.fill();
    // Candy cane stripes
    ctx.fillStyle = '#ffffff';
    ctx.save();
    ctx.beginPath(); ctx.arc(0, 0, 11, 0, Math.PI * 2); ctx.clip();
    ctx.fillRect(-3, -12, 3, 24);
    ctx.fillRect(4, -12, 3, 24);
    ctx.fillRect(-10, -12, 3, 24);
    ctx.restore();
    ctx.restore();
  }

  function drawFrosting(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Pastry bag
    ctx.fillStyle = '#4895ef';
    ctx.beginPath();
    ctx.moveTo(-16, -14);
    ctx.lineTo(8, -14);
    ctx.lineTo(16, 8);
    ctx.lineTo(-4, 8);
    ctx.closePath(); ctx.fill();
    // Metal nozzle
    ctx.fillStyle = '#d8e2dc';
    ctx.fillRect(14, 6, 6, 6);
    // Dollop of cream
    ctx.fillStyle = '#fff0f3';
    ctx.beginPath(); ctx.arc(23, 11, 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffb3c1';
    ctx.beginPath(); ctx.arc(22, 10, 3, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  function drawAnvil(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Cast iron base
    ctx.fillStyle = '#495057';
    ctx.fillRect(-16, 10, 32, 6);
    ctx.fillStyle = '#6c757d';
    ctx.fillRect(-14, 10, 28, 2);
    // Center column
    ctx.fillStyle = '#343a40';
    ctx.fillRect(-10, 2, 20, 8);
    // Horn
    ctx.fillStyle = '#495057';
    ctx.beginPath();
    ctx.moveTo(-10, 2); ctx.lineTo(-24, -4); ctx.lineTo(-10, -4);
    ctx.closePath(); ctx.fill();
    // Top striking plate
    ctx.fillStyle = '#6c757d';
    ctx.fillRect(-12, -6, 30, 8);
    ctx.fillStyle = '#ced4da';
    ctx.fillRect(-12, -6, 30, 2);
    // Weight marking
    ctx.fillStyle = '#ff4646';
    ctx.font = 'bold 7px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('100T', 2, 8);
    ctx.restore();
  }

  function drawBroccoli(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Florets
    ctx.fillStyle = '#2d6a4f';
    [[-12, -6, 9], [0, -14, 11], [12, -6, 9], [-6, -4, 8], [6, -4, 8]].forEach(([bx, by, br]) => {
      ctx.beginPath(); ctx.arc(bx, by, br, 0, Math.PI * 2); ctx.fill();
    });
    ctx.fillStyle = '#52b788';
    [[-10, -8, 6], [0, -15, 7], [10, -8, 6]].forEach(([bx, by, br]) => {
      ctx.beginPath(); ctx.arc(bx, by, br, 0, Math.PI * 2); ctx.fill();
    });
    // Stalk
    ctx.fillStyle = '#74c69d';
    ctx.fillRect(-5, 2, 10, 14);
    // Angry Eyebrows
    ctx.strokeStyle = '#081c15';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(-9, -7); ctx.lineTo(-3, -4);
    ctx.moveTo(9, -7); ctx.lineTo(3, -4);
    ctx.stroke();
    // Eyes
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-8, -4, 4, 4);
    ctx.fillRect(4, -4, 4, 4);
    ctx.fillStyle = '#d00000';
    ctx.fillRect(-7, -3, 2, 2);
    ctx.fillRect(5, -3, 2, 2);
    ctx.restore();
  }

  function drawSpoiledMilk(ctx, x, y, rot, bt) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.5, 1.5);
    // Carton
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(-12, -6, 24, 28);
    ctx.fillStyle = '#e9ecef';
    ctx.beginPath();
    ctx.moveTo(-12, -6); ctx.lineTo(0, -18); ctx.lineTo(12, -6);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#ced4da';
    ctx.fillRect(-3, -21, 6, 4);
    // Sour green label
    ctx.fillStyle = '#70e000';
    ctx.fillRect(-11, 0, 22, 14);
    ctx.fillStyle = '#004b23';
    ctx.font = 'bold 5px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('SOUR', 0, 6);
    ctx.fillText('SPOILED', 0, 11);
    ctx.fillText('MILK', 0, 16);
    // Slime drips
    ctx.fillStyle = '#38b000';
    ctx.fillRect(-9, 20, 5, 6);
    ctx.fillRect(3, 20, 6, 8);
    // Ooze bubbles
    ctx.fillStyle = 'rgba(112, 224, 0, 0.7)';
    const b1 = Math.sin((bt || 0) * 6) * 4;
    ctx.beginPath(); ctx.arc(-14 + b1, -10 - ((bt || 0) * 22 % 28), 3, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(14 - b1, -6 - (((bt || 0) + 0.4) * 22 % 28), 3.5, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  // Update
  let lastTime = performance.now();
  function update(dt) {
    globalTime += dt;
    shakeTime = Math.max(0, shakeTime - dt);

    // Stars
    stars.forEach(s => {
      s.y += s.speed;
      s.twinkle += dt * 3;
      if (s.y > HEIGHT) { s.y = 0; s.x = Math.random() * WIDTH; }
    });

    // Balloons
    balloons.forEach(b => {
      b.y += b.dy;
      b.x += Math.sin(globalTime * 2 + b.phase) * 0.4;
      if (b.y < -50) { b.y = HEIGHT + 30; b.x = Math.random() * WIDTH; }
    });

    // Confetti
    confetti.forEach(c => {
      c.y += c.vy * dt;
      if (c.y > HEIGHT) { c.y = -10; c.x = Math.random() * WIDTH; }
    });

    // Stardust Trails
    trails = trails.filter(t => t.life > 0);
    trails.forEach(t => {
      t.life -= dt * 2.2;
      t.y += t.vy * dt * 0.3;
    });

    // Particles
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
    });

    if (state === 'PLAYING') {
      btnAction.textContent = 'PAUSE';

      // Player Movement (responsive drag + keys + buttons)
      let moveDir = 0;
      if (keys['ArrowLeft'] || keys['KeyA']) moveDir -= 1;
      if (keys['ArrowRight'] || keys['KeyD']) moveDir += 1;

      if (moveDir !== 0) {
        player.x += moveDir * player.speed * dt;
        targetX = player.x;
        player.walkTime += dt * 10;
      } else if (isDragging) {
        const dx = targetX - player.x;
        player.x += dx * Math.min(1.0, 24 * dt);
        player.walkTime += Math.abs(dx) * dt * 0.18;
      }
      player.x = Math.max(player.w / 2, Math.min(WIDTH - player.w / 2, player.x));
      if (player.invincible > 0) player.invincible -= dt;

      // Stage Countdown
      timeLeft -= dt;
      if (timeLeft <= 0) {
        lives--;
        shakeTime = 0.4;
        player.invincible = 1.5;
        addScorePopup(player.x, player.y - 40, "TIME UP!", COLORS.RED);
        sfxHit();
        haptic([60, 40, 60]);
        if (lives <= 0) endGame();
        else timeLeft = STAGE_DURATION;
      }

      // Spawner
      const speed = 190 + (stage - 1) * 30;
      const interval = Math.max(0.38, 1.35 - (stage - 1) * 0.1);
      spawnTimer -= dt;
      if (spawnTimer <= 0) {
        spawnTimer = interval;
        const isBad = Math.random() < Math.min(0.45, 0.28 + (stage - 1) * 0.02);
        const kind = isBad ? BAD_KINDS[Math.floor(Math.random() * BAD_KINDS.length)]
                           : GOOD_KINDS[Math.floor(Math.random() * GOOD_KINDS.length)];
        const minX = Math.min(90, WIDTH * 0.12);
        const maxX = WIDTH - minX;
        items.push({
          x: minX + Math.random() * (maxX - minX),
          y: -40,
          vy: speed,
          isBad: isBad,
          kind: kind,
          pts: GOOD_POINTS[kind] || 0,
          rot: 0,
          vrot: (Math.random() - 0.5) * 4.5,
          color: isBad ? COLORS.RED : (kind === 'CAKE' ? COLORS.PINK : COLORS.GOLD)
        });
      }

      // Cake height dynamically grows with items caught
      const cakeLayersH = (itemsCaughtStage >= 4 ? 68 : (itemsCaughtStage >= 2 ? 38 : 20)) * 1.25;
      const trayRect = {
        x: player.x - 70,
        y: player.y - 92 * 1.25 - cakeLayersH - 14,
        w: 140,
        h: cakeLayersH + 32
      };
      const bodyRect = {
        x: player.x - 22,
        y: player.y - 45,
        w: 44,
        h: 90
      };

      // Emit animated jet spark particles downwards from boots
      if (Math.random() < 0.65) {
        [-15 * 1.25, 15 * 1.25].forEach(bx => {
          particles.push({
            x: player.x + bx + (Math.random() - 0.5) * 4,
            y: player.y + 50 * 1.25,
            vx: (Math.random() - 0.5) * 20,
            vy: 110 + Math.random() * 90,
            life: 0.22,
            maxLife: 0.22,
            color: Math.random() < 0.6 ? '#ffd700' : (Math.random() < 0.5 ? '#ff4da6' : '#00dcff'),
            size: 3
          });
        });
      }

      for (let i = items.length - 1; i >= 0; i--) {
        const item = items[i];
        item.y += item.vy * dt;
        item.rot += item.vrot * dt;

        // Leave stardust trail
        if (Math.random() < 0.35) {
          trails.push({
            x: item.x + (Math.random() - 0.5) * 8,
            y: item.y - 10,
            vy: -15,
            life: 0.8,
            color: item.isBad ? 'rgba(255, 50, 70, 0.6)' : 'rgba(0, 255, 136, 0.6)'
          });
        }

        // Catch check
        if (!item.isBad) {
          if (item.x >= trayRect.x && item.x <= trayRect.x + trayRect.w &&
              item.y >= trayRect.y && item.y <= trayRect.y + trayRect.h + 24) {
            score += 100;
            itemsCaughtStage++;
            addCollectBurst(item.x, item.y, '#00ff88');
            addScorePopup(item.x, item.y - 20, "+100", '#00ff88');
            sfxCatch();
            haptic(15);
            items.splice(i, 1);

            if (itemsCaughtStage >= ITEMS_PER_STAGE) {
              score += 500;
              state = 'STAGE_CLEAR';
              stageClearTime = 1.8;
              addCollectBurst(WIDTH / 2, HEIGHT / 2, COLORS.GOLD);
              sfxWin();
              haptic([30, 30, 60]);
            }
            continue;
          }
        } else {
          // Obstacle collision
          if (player.invincible <= 0) {
            if (item.x >= bodyRect.x && item.x <= bodyRect.x + bodyRect.w &&
                item.y >= bodyRect.y && item.y <= bodyRect.y + bodyRect.h) {
              lives--;
              shakeTime = 0.35;
              player.invincible = 1.5;
              addCollectBurst(item.x, item.y, COLORS.RED);
              addScorePopup(player.x, player.y - 50, "-1 LIFE", "#ff2a55");
              sfxHit();
              haptic([60, 40, 60]);
              items.splice(i, 1);
              if (lives <= 0) endGame();
              continue;
            }
          }
        }

        // Clean off-screen
        if (item.y > HEIGHT + 40) {
          items.splice(i, 1);
        }
      }
    } else if (state === 'STAGE_CLEAR') {
      stageClearTime -= dt;
      if (stageClearTime <= 0) nextStage();
    } else if (state === 'WIN') {
      if (Math.random() < 0.08) {
        addFireworks(100 + Math.random() * (WIDTH - 200), 100 + Math.random() * (HEIGHT * 0.5),
                     bColors[Math.floor(Math.random() * bColors.length)]);
      }
    }
  }

  // Draw
  function draw() {
    ctx.save();
    if (shakeTime > 0) {
      const sx = (Math.random() - 0.5) * 8;
      const sy = (Math.random() - 0.5) * 8;
      ctx.translate(sx, sy);
    }

    // Space Deep Radial Gradient
    const bgGrad = ctx.createRadialGradient(WIDTH / 2, HEIGHT / 2, 50, WIDTH / 2, HEIGHT / 2, HEIGHT * 0.8);
    bgGrad.addColorStop(0, '#1a1040');
    bgGrad.addColorStop(0.65, '#0b0621');
    bgGrad.addColorStop(1, '#050210');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Glowing Nebula clouds
    ctx.save();
    ctx.globalAlpha = 0.18;
    const neb1 = ctx.createRadialGradient(WIDTH * 0.25, HEIGHT * 0.35, 10, WIDTH * 0.25, HEIGHT * 0.35, 260);
    neb1.addColorStop(0, '#ff00aa'); neb1.addColorStop(1, 'transparent');
    ctx.fillStyle = neb1; ctx.fillRect(0, 0, WIDTH, HEIGHT);

    const neb2 = ctx.createRadialGradient(WIDTH * 0.75, HEIGHT * 0.65, 10, WIDTH * 0.75, HEIGHT * 0.65, 280);
    neb2.addColorStop(0, '#00dcff'); neb2.addColorStop(1, 'transparent');
    ctx.fillStyle = neb2; ctx.fillRect(0, 0, WIDTH, HEIGHT);
    ctx.restore();

    // Pixel Stars with sparkling 4-point shape
    stars.forEach(s => {
      ctx.save();
      const alpha = 0.4 + 0.6 * Math.abs(Math.sin(s.twinkle));
      ctx.fillStyle = s.color;
      ctx.globalAlpha = alpha;
      const sz = s.size;
      ctx.fillRect(s.x, s.y, sz, sz);
      if (sz >= 3) {
        ctx.fillRect(s.x - 1, s.y + 1, sz + 2, sz - 2);
        ctx.fillRect(s.x + 1, s.y - 1, sz - 2, sz + 2);
      }
      ctx.restore();
    });

    // Portholes looking into galaxies
    const isPortrait = HEIGHT > WIDTH;
    const portholes = isPortrait
      ? [[80, 280, 52], [WIDTH - 80, 280, 52], [80, 680, 45], [WIDTH - 80, 680, 45]]
      : [[180, 280, 95], [WIDTH - 180, 280, 95], [130, 520, 60], [WIDTH - 130, 520, 60]];

    portholes.forEach(([cx, cy, r]) => {
      ctx.save();
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.clip();
      ctx.fillStyle = COLORS.SPACE_MID; ctx.fill();
      // Galaxy swirl
      ctx.fillStyle = '#b042ff';
      ctx.beginPath(); ctx.arc(cx, cy, r / 3, 0, Math.PI * 2); ctx.fill();
      ctx.restore();

      ctx.strokeStyle = '#3d4d80';
      ctx.lineWidth = 6;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
      ctx.strokeStyle = '#00dcff';
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(cx, cy, r + 4, 0, Math.PI * 2); ctx.stroke();
    });

    // Background Balloons — Dimmed & darkened by ~70% (opacity ~28%)
    ctx.save();
    ctx.globalAlpha = 0.28;
    balloons.forEach(b => {
      ctx.fillStyle = b.color;
      ctx.beginPath();
      ctx.ellipse(b.x, b.y, b.sz, b.sz * 1.35, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.beginPath();
      ctx.ellipse(b.x - b.sz * 0.35, b.y - b.sz * 0.4, b.sz * 0.3, b.sz * 0.4, -0.3, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(160, 160, 180, 0.4)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(b.x, b.y + b.sz * 1.35);
      ctx.lineTo(b.x + 3, b.y + b.sz * 1.35 + 16);
      ctx.stroke();
    });
    ctx.restore();

    // Cockpit Side panels
    const pw = 18;
    ctx.fillStyle = '#10162f';
    ctx.fillRect(0, 0, pw, HEIGHT);
    ctx.fillRect(WIDTH - pw, 0, pw, HEIGHT);
    ctx.strokeStyle = '#00dcff';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, pw, HEIGHT);
    ctx.strokeRect(WIDTH - pw, 0, pw, HEIGHT);

    // Doubled-size pulsating purple neon audio waves / speakers
    const spPulse = Math.sin(globalTime * 9) * 5;
    const spY = HEIGHT - 150;

    // Left Speaker
    ctx.save();
    ctx.shadowColor = '#d020ff';
    ctx.shadowBlur = 22;
    ctx.fillStyle = '#240638';
    ctx.beginPath();
    ctx.arc(10, spY, 26, -Math.PI / 2, Math.PI / 2);
    ctx.fill();
    ctx.strokeStyle = '#e040ff';
    ctx.lineWidth = 4;
    ctx.stroke();
    const lWaves = [46 + spPulse, 68 + spPulse * 1.3, 92 + spPulse * 1.7];
    lWaves.forEach((rw, idx) => {
      ctx.strokeStyle = idx === 0 ? '#ff4da6' : (idx === 1 ? '#e040ff' : '#a000e0');
      ctx.lineWidth = 4.5 - idx * 0.8;
      ctx.beginPath();
      ctx.arc(10, spY, rw, -Math.PI * 0.44, Math.PI * 0.44);
      ctx.stroke();
    });
    ctx.restore();

    // Right Speaker
    ctx.save();
    ctx.shadowColor = '#d020ff';
    ctx.shadowBlur = 22;
    ctx.fillStyle = '#240638';
    ctx.beginPath();
    ctx.arc(WIDTH - 10, spY, 26, Math.PI / 2, Math.PI * 1.5);
    ctx.fill();
    ctx.strokeStyle = '#e040ff';
    ctx.lineWidth = 4;
    ctx.stroke();
    lWaves.forEach((rw, idx) => {
      ctx.strokeStyle = idx === 0 ? '#ff4da6' : (idx === 1 ? '#e040ff' : '#a000e0');
      ctx.lineWidth = 4.5 - idx * 0.8;
      ctx.beginPath();
      ctx.arc(WIDTH - 10, spY, rw, Math.PI * 0.56, Math.PI * 1.44);
      ctx.stroke();
    });
    ctx.restore();

    // Top & Floor Panels
    ctx.fillStyle = '#161e42';
    ctx.fillRect(0, 0, WIDTH, 54);
    ctx.fillStyle = '#0c1024';
    ctx.fillRect(0, HEIGHT - 50, WIDTH, 50);
    ctx.strokeStyle = '#00dcff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 54); ctx.lineTo(WIDTH, 54);
    ctx.moveTo(0, HEIGHT - 50); ctx.lineTo(WIDTH, HEIGHT - 50);
    ctx.stroke();

    // Highlighted "HAPPY BIRTHDAY!" Bunting Banner — Twice as Large
    const letters = "HAPPYBIRTHDAY!".split('');
    const flagColors = ['#9b5de5', '#f15bb5', '#fee440', '#00bbf9', '#00f5d4', '#ff8500', '#9b5de5', '#f15bb5', '#fee440', '#00bbf9', '#00f5d4', '#ff8500', '#f15bb5', '#00bbf9'];
    const xStart = pw + 12, xEnd = WIDTH - pw - 12;
    const fw = (xEnd - xStart) / letters.length;
    const flagW = Math.min(52, fw - 4);
    const flagH = 58;

    // Bunting white suspension cord
    ctx.save();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(xStart, 55);
    for (let i = 0; i < letters.length; i++) {
      const fx = xStart + fw * (i + 0.5);
      const sag = Math.sin((Math.PI * (i + 0.5)) / letters.length) * 16;
      ctx.lineTo(fx, 56 + sag);
    }
    ctx.lineTo(xEnd, 55);
    ctx.stroke();

    // Large colourful flags with bold high-contrast letters
    letters.forEach((l, i) => {
      const fx = xStart + fw * (i + 0.5);
      const sag = Math.sin((Math.PI * (i + 0.5)) / letters.length) * 16;
      const fy = 56 + sag;

      // Triangular Flag
      ctx.fillStyle = flagColors[i % flagColors.length];
      ctx.beginPath();
      ctx.moveTo(fx - flagW / 2, fy);
      ctx.lineTo(fx + flagW / 2, fy);
      ctx.lineTo(fx, fy + flagH);
      ctx.closePath();
      ctx.fill();

      // Sharp white outline
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.8;
      ctx.stroke();

      // Bold white letter with dark shadow
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 15px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.shadowColor = '#000000';
      ctx.shadowBlur = 4;
      ctx.fillText(l, fx, fy + 26);
      ctx.shadowBlur = 0;
    });
    ctx.restore();

    // Stardust Trails
    trails.forEach(t => {
      ctx.save();
      ctx.fillStyle = t.color;
      ctx.globalAlpha = Math.max(0, t.life);
      ctx.fillRect(t.x, t.y, 3, 3);
      ctx.restore();
    });

    // Confetti
    confetti.forEach(c => {
      ctx.fillStyle = c.color;
      ctx.fillRect(c.x, c.y, c.sz, c.sz * 1.6);
    });

    // Falling Items with Glowing Auras
    items.forEach(item => {
      ctx.save();
      const trailH = 80;
      const grad = ctx.createLinearGradient(item.x, item.y - trailH, item.x, item.y + 15);
      if (item.isBad) {
        // Warning-red trail / glowing halo
        grad.addColorStop(0, 'rgba(255, 30, 60, 0)');
        grad.addColorStop(0.65, 'rgba(255, 40, 70, 0.25)');
        grad.addColorStop(1, 'rgba(255, 20, 50, 0.55)');
        ctx.fillStyle = grad;
        ctx.fillRect(item.x - 26, item.y - trailH, 52, trailH + 20);
        ctx.shadowColor = '#ff2040';
        ctx.shadowBlur = 18;
      } else {
        // Faint glowing green trail / particle aura
        grad.addColorStop(0, 'rgba(0, 255, 136, 0)');
        grad.addColorStop(0.65, 'rgba(0, 255, 136, 0.22)');
        grad.addColorStop(1, 'rgba(0, 255, 136, 0.48)');
        ctx.fillStyle = grad;
        ctx.fillRect(item.x - 24, item.y - trailH, 48, trailH + 20);
        ctx.shadowColor = '#00ff88';
        ctx.shadowBlur = 16;
      }

      // 1.5x scaled pixel items
      if (item.kind === 'CAKE') drawCake(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'CANDY') drawCandy(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'STRAWBERRY') drawStrawberry(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'CHERRY') drawCherry(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'CANDLE') drawCandle(ctx, item.x, item.y, item.rot, globalTime);
      else if (item.kind === 'FROSTING') drawFrosting(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'ANVIL') drawAnvil(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'BROCCOLI') drawBroccoli(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'SPOILED_MILK') drawSpoiledMilk(ctx, item.x, item.y, item.rot, globalTime);
      ctx.restore();
    });

    // Playable Character (Aisha) — Scaled 1.25x with dynamic growing cake
    if (state === 'PLAYING' || state === 'STAGE_CLEAR' || state === 'PAUSED') {
      const flicker = player.invincible > 0 && Math.floor(player.invincible * 14) % 2 === 0;
      if (!flicker) {
        ctx.save();
        const bob = Math.sin(player.walkTime) * 3;
        const px = player.x;
        const py = player.y + bob;

        ctx.translate(px, py);
        ctx.scale(1.25, 1.25);

        // 1. Boot Thrusters with Animated Pixel-Jet Flame Cones
        [-15, 15].forEach(bx => {
          ctx.fillStyle = '#00dcff';
          ctx.fillRect(bx - 5, 46, 10, 4);
          const flick = (Math.sin(globalTime * 35 + bx) + 1) * 0.5;
          const flameLen = 10 + flick * 12;
          ctx.fillStyle = '#ff6600';
          ctx.beginPath();
          ctx.moveTo(bx - 5, 50); ctx.lineTo(bx + 5, 50); ctx.lineTo(bx, 50 + flameLen);
          ctx.closePath(); ctx.fill();
          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.moveTo(bx - 2.5, 50); ctx.lineTo(bx + 2.5, 50); ctx.lineTo(bx, 50 + flameLen * 0.6);
          ctx.closePath(); ctx.fill();
        });

        // 2. High-top Sneakers & Denim Jeans
        ctx.fillStyle = COLORS.ORANGE;
        ctx.fillRect(-18, 38, 14, 8);
        ctx.fillRect(4, 38, 14, 8);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-17, 44, 12, 2);
        ctx.fillRect(5, 44, 12, 2);

        ctx.fillStyle = '#2b5894';
        ctx.fillRect(-16, 14, 13, 25);
        ctx.fillRect(3, 14, 13, 25);

        // Belt & Buckle
        ctx.fillStyle = '#261405';
        ctx.fillRect(-16, 9, 32, 5);
        ctx.fillStyle = '#ffd700';
        ctx.fillRect(-4, 9, 8, 5);

        // 3. Signature Floral Blouse & Baker Apron
        ctx.fillStyle = '#f8f2e6';
        ctx.fillRect(-16, -14, 32, 24);
        ctx.fillStyle = '#f4a261';
        ctx.fillRect(-12, -4, 24, 14);
        ctx.fillStyle = '#c9184a';
        ctx.beginPath();
        ctx.arc(-8, -8, 2, 0, Math.PI * 2);
        ctx.arc(8, -6, 2, 0, Math.PI * 2);
        ctx.arc(-6, 2, 1.8, 0, Math.PI * 2);
        ctx.arc(7, 3, 1.8, 0, Math.PI * 2);
        ctx.fill();

        // 4. Raised Arms Reaching Up to Plate
        ctx.strokeStyle = '#f8f2e6';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(-18, -10); ctx.lineTo(-28, -50);
        ctx.moveTo(18, -10); ctx.lineTo(28, -50);
        ctx.stroke();
        ctx.strokeStyle = '#f4a261';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(-28, -50); ctx.lineTo(-36, -90);
        ctx.moveTo(28, -50); ctx.lineTo(36, -90);
        ctx.stroke();

        // 5. Aisha Head — Cropped into an oval with a blue retro outline
        const headY = -36;
        const headRx = 20;
        const headRy = 26;

        ctx.save();
        ctx.shadowColor = '#00dcff';
        ctx.shadowBlur = 10;
        ctx.strokeStyle = '#00dcff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(0, headY, headRx, headRy, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        ctx.save();
        ctx.beginPath();
        ctx.ellipse(0, headY, headRx, headRy, 0, 0, Math.PI * 2);
        ctx.clip();
        if (aishaHead.complete && aishaHead.naturalWidth > 0) {
          ctx.drawImage(aishaHead, -headRx - 2, headY - headRy - 2, (headRx + 2) * 2, (headRy + 3) * 2);
        } else if (aishaPortrait.complete && aishaPortrait.naturalWidth > 0) {
          ctx.drawImage(aishaPortrait, -headRx - 2, headY - headRy - 2, (headRx + 2) * 2, (headRy + 3) * 2);
        }
        ctx.restore();

        // 6. Pink Party Hat Seated Directly on Top of Hair
        const hatBaseY = headY - headRy + 3;
        const hatTipY = hatBaseY - 26;
        ctx.fillStyle = '#ff4da6';
        ctx.beginPath();
        ctx.moveTo(-13, hatBaseY);
        ctx.lineTo(13, hatBaseY);
        ctx.lineTo(0, hatTipY);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-5, hatBaseY - 9, 3, 3);
        ctx.fillRect(4, hatBaseY - 14, 3, 3);
        ctx.fillRect(-1, hatBaseY - 20, 2, 2);
        ctx.beginPath();
        ctx.arc(0, hatTipY - 2, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // 7. Wide Silver Catch Tray Held Right Above Party Hat
        const trayW = 110;
        const trayH = 10;
        const trayY = -92;
        ctx.fillStyle = '#b0c4de';
        ctx.fillRect(-trayW / 2, trayY, trayW, trayH);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-trayW / 2 + 4, trayY + 1, trayW - 8, 2);
        ctx.fillStyle = '#6c757d';
        ctx.fillRect(-trayW / 2, trayY + trayH - 2, trayW, 2);
        ctx.strokeStyle = '#00dcff';
        ctx.lineWidth = 1.5;
        ctx.strokeRect(-trayW / 2, trayY, trayW, trayH);

        // 8. Multi-Layered Cake Dynamically Growing on Tray
        // Tier 1 Base Layer (always present)
        const t1W = 76, t1H = 18;
        const t1Y = trayY - t1H;
        ctx.fillStyle = '#ff4da6';
        ctx.fillRect(-t1W / 2, t1Y, t1W, t1H);
        ctx.fillStyle = '#00dcff';
        for (let ix = -t1W / 2; ix < t1W / 2; ix += 8) {
          ctx.beginPath();
          ctx.arc(ix + 4, t1Y + t1H, 4, Math.PI, 0);
          ctx.fill();
        }
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-24, t1Y + 5, 3, 3);
        ctx.fillRect(-4, t1Y + 8, 3, 3);
        ctx.fillRect(16, t1Y + 4, 3, 3);

        // Tier 2 Layer (grows if itemsCaughtStage >= 2)
        if (itemsCaughtStage >= 2) {
          const t2W = 58, t2H = 16;
          const t2Y = t1Y - t2H;
          ctx.fillStyle = '#f4a261';
          ctx.fillRect(-t2W / 2, t2Y, t2W, t2H);
          ctx.fillStyle = '#fff3b0';
          ctx.fillRect(-t2W / 2, t2Y + 4, t2W, 3);
          ctx.fillStyle = '#ff4da6';
          for (let ix = -t2W / 2; ix < t2W / 2; ix += 8) {
            ctx.beginPath();
            ctx.arc(ix + 4, t2Y + t2H, 3.5, Math.PI, 0);
            ctx.fill();
          }
        }

        // Tier 3 Layer (grows if itemsCaughtStage >= 4)
        if (itemsCaughtStage >= 4) {
          const t3W = 42, t3H = 14;
          const t3Y = t1Y - 16 - t3H;
          ctx.fillStyle = '#c040ff';
          ctx.fillRect(-t3W / 2, t3Y, t3W, t3H);
          ctx.fillStyle = '#00dcff';
          ctx.fillRect(-t3W / 2, t3Y + 3, t3W, 2);
        }

        // Birthday Candles (flickering on top of highest layer)
        const topY = itemsCaughtStage >= 4 ? (t1Y - 30) : (itemsCaughtStage >= 2 ? (t1Y - 16) : t1Y);
        const candleColors = ['#ff4da6', '#ffd700', '#00dcff'];
        [-12, 0, 12].forEach((cx, idx) => {
          ctx.fillStyle = candleColors[idx % candleColors.length];
          ctx.fillRect(cx - 2, topY - 12, 4, 12);
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(cx - 0.5, topY - 14, 1, 2);
          const cFlick = Math.sin(globalTime * 18 + idx) * 1.5;
          ctx.fillStyle = '#ffd700';
          ctx.beginPath();
          ctx.ellipse(cx, topY - 17 + cFlick * 0.5, 2.5, 4, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(cx - 1, topY - 18 + cFlick * 0.5, 2, 2);
        });

        ctx.restore();
      }
    }

    // Particles & Floating Text Popups
    particles.forEach(p => {
      ctx.save();
      const alpha = Math.max(0, p.life / p.maxLife);
      if (p.isText) {
        ctx.fillStyle = p.color;
        ctx.font = '14px "Press Start 2P", monospace';
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000';
        ctx.shadowBlur = 6;
        ctx.fillText(p.text, p.x, p.y);
      } else {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    });

    // ─── RETRO 16-BIT HUD ─────────────────────────────────────────────
    // Top Score Box — Sharp Bright Yellow
    ctx.save();
    ctx.fillStyle = '#ffd700';
    ctx.shadowColor = 'rgba(255, 215, 0, 0.6)';
    ctx.shadowBlur = 8;
    ctx.font = '14px "Press Start 2P", monospace';
    ctx.textAlign = 'left';
    ctx.fillText("SCORE: " + String(score).padStart(6, "0"), pw + 32, 35);
    ctx.restore();

    // Center Timer — Sharp Bright Cyan
    ctx.save();
    const secs = Math.max(0, Math.ceil(timeLeft));
    const tStr = "0:" + String(secs).padStart(2, "0");
    const tCol = (timeLeft < 10 && Math.floor(globalTime * 4) % 2 === 0) ? '#ff2a55' : '#00dcff';
    ctx.fillStyle = tCol;
    ctx.shadowColor = tCol;
    ctx.shadowBlur = 8;
    ctx.font = '16px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(tStr, WIDTH / 2, 35);
    ctx.restore();

    // Pixel Hearts (Lives) — Top Right
    const hx = WIDTH - pw - 60;
    for (let i = 0; i < MAX_LIVES; i++) {
      const active = i < lives;
      const lx = hx - (MAX_LIVES - 1 - i) * 28;
      ctx.save();
      ctx.fillStyle = active ? '#ff2a55' : '#331520';
      if (active) {
        ctx.shadowColor = '#ff2a55';
        ctx.shadowBlur = 8;
      }
      ctx.fillRect(lx - 10, 22, 9, 9);
      ctx.fillRect(lx - 1, 22, 9, 9);
      ctx.fillRect(lx - 9, 31, 16, 7);
      ctx.fillRect(lx - 5, 38, 8, 4);
      if (active) {
        ctx.fillStyle = '#ffb3c6';
        ctx.fillRect(lx - 8, 24, 3, 3);
      }
      ctx.restore();
    }

    // Bottom Bar: "ZERO-G MODE" in Neon Cyan & "STAGE X/10" in Neon Orange
    ctx.save();
    ctx.fillStyle = '#00dcff';
    ctx.shadowColor = '#00dcff';
    ctx.shadowBlur = 10;
    ctx.font = '13px "Press Start 2P", monospace';
    ctx.textAlign = 'left';
    ctx.fillText("ZERO-G MODE", pw + 18, HEIGHT - 20);
    ctx.restore();

    // Animated Neon Sine Wave Oscillation
    ctx.strokeStyle = '#00dcff';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    const waveStart = pw + 180;
    const waveWidth = Math.max(100, WIDTH - pw * 2 - 370);
    for (let wx = 0; wx < waveWidth; wx += 4) {
      const wy = HEIGHT - 23 + Math.sin(wx * 0.08 + globalTime * 7) * 7;
      if (wx === 0) ctx.moveTo(waveStart + wx, wy);
      else ctx.lineTo(waveStart + wx, wy);
    }
    ctx.stroke();

    ctx.save();
    ctx.fillStyle = '#ff9900';
    ctx.shadowColor = '#ffaa00';
    ctx.shadowBlur = 10;
    ctx.font = '13px "Press Start 2P", monospace';
    ctx.textAlign = 'right';
    ctx.fillText("STAGE " + stage + "/" + TOTAL_STAGES, WIDTH - pw - 18, HEIGHT - 20);
    ctx.restore();

    // ─── OVERLAY SCREENS ──────────────────────────────────────────────
    const boxW = Math.min(WIDTH - 36, 680);
    const boxH = Math.min(HEIGHT - 120, 420);

    if (state === 'MENU') {
      btnAction.textContent = 'START';
      const boxW = 660;
      const boxH = 530;
      const boxX = WIDTH / 2 - boxW / 2;
      const boxY = HEIGHT / 2 - boxH / 2;

      ctx.fillStyle = 'rgba(10, 6, 32, 0.95)';
      ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 4;
      ctx.strokeRect(boxX, boxY, boxW, boxH);

      // Gold Corner Accent Pixels
      ctx.fillStyle = COLORS.CYAN;
      [[boxX, boxY], [boxX + boxW - 12, boxY], [boxX, boxY + boxH - 12], [boxX + boxW - 12, boxY + boxH - 12]].forEach(([cxo, cyo]) => {
        ctx.fillRect(cxo, cyo, 12, 12);
      });

      // Top Title Banner
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '18px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("★ AISHA'S ★", WIDTH / 2, boxY + 36);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '15px "Press Start 2P", monospace';
      ctx.fillText("BIRTHDAY BAKE-OFF!", WIDTH / 2, boxY + 64);

      // Centerpiece Portrait of Aisha (Floating 16-bit framed portrait)
      const floatY = Math.sin(globalTime * 2.2) * 5;
      const portW = 180;
      const portH = 240;
      const portY = boxY + 200;
      drawAishaPortrait(ctx, WIDTH / 2, portY, portW, portH, floatY);

      // Birthday Girl Ribbon Tag
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("★ THE BIRTHDAY GIRL ★", WIDTH / 2, portY + portH / 2 + 22 + floatY);

      // Instructions
      ctx.fillStyle = '#c8d4f0';
      ctx.font = '10px "Press Start 2P", monospace';
      ctx.fillText("CATCH FALLING CAKES - DODGE ANVILS!", WIDTH / 2, boxY + 396);

      // Flashing Start Prompt
      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '14px "Press Start 2P", monospace';
      ctx.fillText("▶ TAP SCREEN TO PLAY ◀", WIDTH / 2, boxY + 440);

      // Controls hint
      ctx.fillStyle = '#859bb8';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.fillText("BEST: " + hiScore.toLocaleString() + "   |   TAP ARROWS OR GLIDE THUMB", WIDTH / 2, boxY + 485);
    } else if (state === 'PAUSED') {
      btnAction.textContent = 'RESUME';
      ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '24px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("— PAUSED —", WIDTH / 2, HEIGHT / 2 - 20);
      ctx.fillStyle = COLORS.CYAN;
      ctx.font = '12px "Press Start 2P", monospace';
      ctx.fillText("TAP SCREEN TO RESUME", WIDTH / 2, HEIGHT / 2 + 35);
    } else if (state === 'STAGE_CLEAR') {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '22px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("STAGE " + stage + " CLEAR!", WIDTH / 2, HEIGHT / 2 - 20);
      ctx.fillStyle = COLORS.CYAN;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("GET READY...", WIDTH / 2, HEIGHT / 2 + 35);
    } else if (state === 'GAME_OVER') {
      btnAction.textContent = 'RETRY';
      const boxW = 660;
      const boxH = 530;
      const boxX = WIDTH / 2 - boxW / 2;
      const boxY = HEIGHT / 2 - boxH / 2;

      ctx.fillStyle = 'rgba(45, 5, 12, 0.95)';
      ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.strokeStyle = COLORS.RED;
      ctx.lineWidth = 4;
      ctx.strokeRect(boxX, boxY, boxW, boxH);

      // Corner Accents
      ctx.fillStyle = COLORS.GOLD;
      [[boxX, boxY], [boxX + boxW - 12, boxY], [boxX, boxY + boxH - 12], [boxX + boxW - 12, boxY + boxH - 12]].forEach(([cxo, cyo]) => {
        ctx.fillRect(cxo, cyo, 12, 12);
      });

      ctx.fillStyle = COLORS.RED;
      ctx.font = '20px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("CAKE DISASTER!", WIDTH / 2, boxY + 40);

      // Aisha Portrait on game over
      drawAishaPortrait(ctx, WIDTH / 2, boxY + 185, 135, 180, 0);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("DON'T GIVE UP ON AISHA'S CAKE!", WIDTH / 2, boxY + 300);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '12px "Press Start 2P", monospace';
      ctx.fillText("Score: " + score.toLocaleString(), WIDTH / 2, boxY + 348);
      ctx.fillStyle = COLORS.GOLD;
      ctx.fillText("Hi-Score: " + hiScore.toLocaleString(), WIDTH / 2, boxY + 382);

      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '14px "Press Start 2P", monospace';
      ctx.fillText("▶ TAP TO RETRY ◀", WIDTH / 2, boxY + 440);
    } else if (state === 'WIN') {
      btnAction.textContent = 'AGAIN';
      const boxW = 660;
      const boxH = 530;
      const boxX = WIDTH / 2 - boxW / 2;
      const boxY = HEIGHT / 2 - boxH / 2;

      ctx.fillStyle = 'rgba(10, 6, 32, 0.95)';
      ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 4;
      ctx.strokeRect(boxX, boxY, boxW, boxH);

      // Gold Corner Accent Pixels
      ctx.fillStyle = COLORS.CYAN;
      [[boxX, boxY], [boxX + boxW - 12, boxY], [boxX, boxY + boxH - 12], [boxX + boxW - 12, boxY + boxH - 12]].forEach(([cxo, cyo]) => {
        ctx.fillRect(cxo, cyo, 12, 12);
      });

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '18px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("★ CHAMPION BAKER! ★", WIDTH / 2, boxY + 36);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '15px "Press Start 2P", monospace';
      ctx.fillText("HAPPY BIRTHDAY AISHA! 🎂", WIDTH / 2, boxY + 64);

      const floatY = Math.sin(globalTime * 2.2) * 5;
      const portW = 180;
      const portH = 240;
      const portY = boxY + 200;
      drawAishaPortrait(ctx, WIDTH / 2, portY, portW, portH, floatY);

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("★ BIRTHDAY WISH GRANTED! ★", WIDTH / 2, portY + portH / 2 + 22 + floatY);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '12px "Press Start 2P", monospace';
      ctx.fillText("FINAL SCORE: " + score.toLocaleString(), WIDTH / 2, boxY + 396);

      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("★ TAP TO PLAY AGAIN ★", WIDTH / 2, boxY + 440);
    }

    ctx.restore();
  }

  function loop(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;
    update(dt);
    draw();
    requestAnimationFrame(loop);
  }

  syncUIState();
  handleResize();
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

with open("assets/aisha_portrait.jpg", "rb") as f:
    portrait_b64 = base64.b64encode(f.read()).decode("ascii")

with open("assets/aisha_head.png", "rb") as f:
    head_b64 = base64.b64encode(f.read()).decode("ascii")

html = html.replace("%%AISHA_PORTRAIT_B64%%", portrait_b64)
html = html.replace("%%AISHA_HEAD_B64%%", head_b64)

with open("game.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully compiled ultra-quality retro pixel game.html with Aisha centerpiece! Size:", len(html))
