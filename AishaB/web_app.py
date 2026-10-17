# web_app.py — Web entrypoint & browser-playable edition of Anti-Gravity Birthday Bake-Off
#
# Provides WSGI, ASGI, and serverless handlers:
#   • app          (WSGI + ASGI compatible hybrid)
#   • application  (WSGI alias)
#   • handler      (AWS Lambda / Serverless function handler)


HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Anti-Gravity Birthday Bake-Off 🎂</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body {
    background: #0f0a2d;
    color: #fff;
    font-family: 'Courier New', monospace;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
  }
  #container {
    position: relative;
    width: 100%;
    max-width: 1280px;
    aspect-ratio: 16 / 9;
    box-shadow: 0 10px 40px rgba(0, 220, 255, 0.25);
    border: 3px solid #00dcff;
    border-radius: 8px;
    overflow: hidden;
    background: #0f0a2d;
  }
  canvas {
    width: 100%;
    height: 100%;
    display: block;
    image-rendering: pixelated;
  }
  .touch-controls {
    display: none;
    position: absolute;
    bottom: 20px;
    width: 100%;
    padding: 0 30px;
    justify-content: space-between;
    pointer-events: none;
  }
  .touch-btn {
    pointer-events: auto;
    background: rgba(0, 220, 255, 0.3);
    border: 2px solid #00dcff;
    color: #fff;
    font-size: 28px;
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    active:scale(0.95);
  }
  @media (pointer: coarse) {
    .touch-controls { display: flex; }
  }
  #info-bar {
    margin-top: 10px;
    font-size: 14px;
    color: #a0c0e0;
    text-align: center;
  }
  #info-bar kbd {
    background: #1e2a50;
    border: 1px solid #406090;
    border-radius: 4px;
    padding: 2px 6px;
    color: #ffd700;
  }
</style>
</head>
<body>

<div id="container">
  <canvas id="gameCanvas" width="1280" height="720"></canvas>
  <div class="touch-controls">
    <div style="display:flex; gap:15px;">
      <button class="touch-btn" id="btn-left">◀</button>
      <button class="touch-btn" id="btn-right">▶</button>
    </div>
    <button class="touch-btn" id="btn-action" style="width:100px; border-radius:35px; font-size:18px;">START</button>
  </div>
</div>

<div id="info-bar">
  Controls: <kbd>A</kbd> / <kbd>D</kbd> or <kbd>←</kbd> / <kbd>→</kbd> Move &nbsp;|&nbsp;
  <kbd>SPACE</kbd> Start/Confirm &nbsp;|&nbsp;
  <kbd>ESC</kbd> Pause
</div>

<script>
(() => {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Audio Context (Synthesizer)
  let audioCtx = null;
  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
  }
  function playBeep(freq, type, duration, gainVal=0.1) {
    if (!audioCtx) return;
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
    playBeep(520, 'triangle', 0.1, 0.15);
    setTimeout(() => playBeep(780, 'triangle', 0.12, 0.15), 50);
  }
  function sfxHit() {
    initAudio();
    playBeep(140, 'sawtooth', 0.25, 0.25);
  }
  function sfxWin() {
    initAudio();
    [400, 500, 600, 800].forEach((f, i) => {
      setTimeout(() => playBeep(f, 'sine', 0.15, 0.2), i * 120);
    });
  }

  // Constants
  const WIDTH = 1280;
  const HEIGHT = 720;
  const TOTAL_STAGES = 10;
  const ITEMS_PER_STAGE = 10;
  const STAGE_DURATION = 38;
  const MAX_LIVES = 3;

  // Colors
  const COLORS = {
    SPACE_DARK: '#0f0a2d',
    SPACE_MID: '#191246',
    COCKPIT_BLUE: '#374682',
    COCKPIT_DARK: '#1e2650',
    COCKPIT_MID: '#2d3a69',
    CYAN: '#00dcff',
    PINK: '#ff6ebe',
    GOLD: '#ffd700',
    RED: '#ff4646',
    WHITE: '#ffffff',
    ORANGE: '#ff9100',
    GREEN: '#37be46',
    PURPLE: '#a03ce6'
  };

  // State
  let state = 'MENU'; // MENU, PLAYING, STAGE_CLEAR, PAUSED, GAME_OVER, WIN
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
    x: WIDTH / 2,
    y: HEIGHT - 105,
    w: 60,
    h: 110,
    speed: 400,
    invincible: 0,
    walkTime: 0
  };

  // Input
  const keys = {};
  window.addEventListener('keydown', (e) => {
    initAudio();
    keys[e.code] = true;
    if (e.code === 'Space') {
      if (state === 'MENU' || state === 'GAME_OVER' || state === 'WIN') {
        startGame();
      }
    }
    if (e.code === 'Escape') {
      if (state === 'PLAYING') state = 'PAUSED';
      else if (state === 'PAUSED') state = 'PLAYING';
    }
    if (e.code === 'KeyQ' && state === 'PAUSED') {
      state = 'MENU';
    }
  });
  window.addEventListener('keyup', (e) => { keys[e.code] = false; });

  // Touch handlers
  const btnL = document.getElementById('btn-left');
  const btnR = document.getElementById('btn-right');
  const btnA = document.getElementById('btn-action');
  const bindTouch = (elem, code) => {
    elem.addEventListener('touchstart', (e) => { e.preventDefault(); initAudio(); keys[code] = true; });
    elem.addEventListener('touchend', (e) => { e.preventDefault(); keys[code] = false; });
  };
  bindTouch(btnL, 'ArrowLeft');
  bindTouch(btnR, 'ArrowRight');
  btnA.addEventListener('click', () => {
    initAudio();
    if (state === 'MENU' || state === 'GAME_OVER' || state === 'WIN') startGame();
    else if (state === 'PLAYING') state = 'PAUSED';
    else if (state === 'PAUSED') state = 'PLAYING';
  });

  // Background layers
  const stars = [];
  for (let i = 0; i < 180; i++) {
    stars.push({
      x: Math.random() * WIDTH,
      y: Math.random() * HEIGHT,
      size: Math.random() < 0.6 ? 1 : (Math.random() < 0.8 ? 2 : 3),
      speed: 0.1 + Math.random() * 0.5,
      alpha: 0.3 + Math.random() * 0.7
    });
  }

  const balloons = [];
  const bColors = [COLORS.PINK, COLORS.CYAN, COLORS.GOLD, COLORS.PURPLE, COLORS.GREEN, COLORS.ORANGE];
  for (let i = 0; i < 12; i++) {
    balloons.push({
      x: Math.random() * WIDTH,
      y: Math.random() * HEIGHT,
      sz: 18 + Math.random() * 12,
      dy: -0.5 - Math.random() * 0.6,
      color: bColors[Math.floor(Math.random() * bColors.length)],
      phase: Math.random() * Math.PI * 2
    });
  }

  // Falling Items & Hazards
  let items = [];
  let spawnTimer = 0.5;

  const GOOD_TYPES = [
    { name: 'CakeTier', pts: 200, color: '#f5deb3', radius: 18, emoji: '🍰' },
    { name: 'Candle', pts: 100, color: '#ff4646', radius: 14, emoji: '🕯️' },
    { name: 'Strawberry', pts: 150, color: '#ff2050', radius: 16, emoji: '🍓' },
    { name: 'Cherry', pts: 180, color: '#dc143c', radius: 15, emoji: '🍒' },
    { name: 'Candy', pts: 120, color: '#ff69b4', radius: 14, emoji: '🍬' },
    { name: 'Frosting', pts: 220, color: '#ffffff', radius: 16, emoji: '🧁' },
  ];

  const BAD_TYPES = [
    { name: 'Anvil', color: '#707888', radius: 20, emoji: '⚡' },
    { name: 'Broccoli', color: '#2e8b57', radius: 18, emoji: '🥦' },
    { name: 'SpoiledMilk', color: '#5ad232', radius: 18, emoji: '🥛' }
  ];

  // Particles
  let particles = [];
  function addCollectBurst(x, y, color) {
    for (let i = 0; i < 16; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 60 + Math.random() * 140;
      particles.push({
        x, y,
        vx: Math.cos(angle) * spd,
        vy: Math.sin(angle) * spd,
        life: 0.5,
        maxLife: 0.5,
        color: color,
        size: 3 + Math.random() * 3
      });
    }
  }

  function addScorePopup(x, y, text, color=COLORS.GOLD) {
    particles.push({
      x, y,
      vx: 0,
      vy: -40,
      life: 0.8,
      maxLife: 0.8,
      text: text,
      color: color,
      isText: true
    });
  }

  function addFireworks(x, y, color) {
    for (let i = 0; i < 28; i++) {
      const angle = Math.random() * Math.PI * 2;
      const spd = 80 + Math.random() * 200;
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

  // Confetti
  const confetti = [];
  for (let i = 0; i < 80; i++) {
    confetti.push({
      x: Math.random() * WIDTH,
      y: Math.random() * HEIGHT,
      vy: 40 + Math.random() * 60,
      color: bColors[Math.floor(Math.random() * bColors.length)],
      sz: 3 + Math.random() * 4,
      rot: Math.random() * 6
    });
  }

  function startGame() {
    score = 0;
    lives = MAX_LIVES;
    stage = 1;
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    shakeTime = 0;
    items = [];
    particles = [];
    player.x = WIDTH / 2;
    player.invincible = 0;
    state = 'PLAYING';
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
      sfxWin();
    } else {
      itemsCaughtStage = 0;
      timeLeft = STAGE_DURATION;
      items = [];
      state = 'PLAYING';
    }
  }

  function endGame() {
    if (score > hiScore) {
      hiScore = score;
      localStorage.setItem('anti_grav_hiscore', hiScore);
    }
    state = 'GAME_OVER';
  }

  // Update loop
  let lastTime = performance.now();
  function update(dt) {
    globalTime += dt;
    shakeTime = Math.max(0, shakeTime - dt);

    // Stars
    stars.forEach(s => {
      s.y += s.speed;
      if (s.y > HEIGHT) s.y = 0;
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

    // Particles
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
    });

    if (state === 'PLAYING') {
      // Player movement
      let move = 0;
      if (keys['ArrowLeft'] || keys['KeyA']) move -= 1;
      if (keys['ArrowRight'] || keys['KeyD']) move += 1;
      player.x += move * player.speed * dt;
      player.x = Math.max(player.w / 2, Math.min(WIDTH - player.w / 2, player.x));
      if (move !== 0) player.walkTime += dt * 10;
      if (player.invincible > 0) player.invincible -= dt;

      // Timer
      timeLeft -= dt;
      if (timeLeft <= 0) {
        lives--;
        shakeTime = 0.4;
        player.invincible = 1.5;
        addScorePopup(player.x, player.y - 40, "TIME UP!", COLORS.RED);
        sfxHit();
        if (lives <= 0) endGame();
        else timeLeft = STAGE_DURATION;
      }

      // Spawner
      const speed = 180 + (stage - 1) * 28;
      const interval = Math.max(0.4, 1.4 - (stage - 1) * 0.1);
      spawnTimer -= dt;
      if (spawnTimer <= 0) {
        spawnTimer = interval;
        const isBad = Math.random() < Math.min(0.45, 0.28 + (stage - 1) * 0.02);
        const template = isBad ? BAD_TYPES[Math.floor(Math.random() * BAD_TYPES.length)]
                               : GOOD_TYPES[Math.floor(Math.random() * GOOD_TYPES.length)];
        items.push({
          x: 160 + Math.random() * (WIDTH - 320),
          y: -30,
          vy: speed,
          isBad: isBad,
          ...template,
          rot: 0,
          vrot: (Math.random() - 0.5) * 5
        });
      }

      // Items update & collision
      const trayRect = {
        x: player.x - 35,
        y: player.y - 50 - 7,
        w: 70,
        h: 14
      };
      const bodyRect = {
        x: player.x - 16,
        y: player.y - 20,
        w: 32,
        h: 70
      };

      for (let i = items.length - 1; i >= 0; i--) {
        const item = items[i];
        item.y += item.vy * dt;
        item.rot += item.vrot * dt;

        // Catch check (Good items)
        if (!item.isBad) {
          if (item.x >= trayRect.x && item.x <= trayRect.x + trayRect.w &&
              item.y >= trayRect.y && item.y <= trayRect.y + trayRect.h + 20) {
            score += item.pts;
            itemsCaughtStage++;
            addCollectBurst(item.x, item.y, item.color);
            addScorePopup(item.x, item.y - 15, `+${item.pts}`, COLORS.GOLD);
            sfxCatch();
            items.splice(i, 1);

            if (itemsCaughtStage >= ITEMS_PER_STAGE) {
              score += 500;
              state = 'STAGE_CLEAR';
              stageClearTime = 1.8;
              addCollectBurst(WIDTH / 2, HEIGHT / 2, COLORS.GOLD);
              sfxWin();
            }
            continue;
          }
        } else {
          // Obstacle check
          if (player.invincible <= 0) {
            if (item.x >= bodyRect.x && item.x <= bodyRect.x + bodyRect.w &&
                item.y >= bodyRect.y && item.y <= bodyRect.y + bodyRect.h) {
              lives--;
              shakeTime = 0.35;
              player.invincible = 1.5;
              addCollectBurst(item.x, item.y, COLORS.RED);
              addScorePopup(item.x, item.y - 20, "OUCH!", COLORS.RED);
              sfxHit();
              items.splice(i, 1);
              if (lives <= 0) endGame();
              continue;
            }
          }
        }

        // Cleanup offscreen
        if (item.y > HEIGHT + 40) {
          items.splice(i, 1);
        }
      }
    } else if (state === 'STAGE_CLEAR') {
      stageClearTime -= dt;
      if (stageClearTime <= 0) nextStage();
    } else if (state === 'WIN') {
      if (Math.random() < 0.08) {
        addFireworks(200 + Math.random() * (WIDTH - 400), 100 + Math.random() * 300,
                     bColors[Math.floor(Math.random() * bColors.length)]);
      }
    }
  }

  // Draw loop
  function draw() {
    ctx.save();
    if (shakeTime > 0) {
      const sx = (Math.random() - 0.5) * 8;
      const sy = (Math.random() - 0.5) * 8;
      ctx.translate(sx, sy);
    }

    // Space Background
    ctx.fillStyle = COLORS.SPACE_DARK;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Stars
    stars.forEach(s => {
      ctx.fillStyle = `rgba(255, 255, 255, ${s.alpha})`;
      ctx.fillRect(s.x, s.y, s.size, s.size);
    });

    // Portholes looking into cosmic galaxy
    const portholes = [[200, 300, 120], [WIDTH - 200, 300, 120], [140, 540, 70], [WIDTH - 140, 540, 70]];
    portholes.forEach(([cx, cy, r]) => {
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.clip();
      ctx.fillStyle = COLORS.SPACE_MID;
      ctx.fill();

      // Galaxy swirl
      ctx.fillStyle = '#a050c8';
      ctx.beginPath();
      ctx.arc(cx, cy, r / 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Porthole rim
      ctx.strokeStyle = COLORS.COCKPIT_MID;
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
    });

    // Balloons
    balloons.forEach(b => {
      ctx.fillStyle = b.color;
      ctx.beginPath();
      ctx.ellipse(b.x, b.y, b.sz, b.sz * 1.35, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#a0a0b4';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(b.x, b.y + b.sz * 1.35);
      ctx.lineTo(b.x + 5, b.y + b.sz * 1.35 + 18);
      ctx.stroke();
    });

    // Cockpit Side panels
    ctx.fillStyle = COLORS.COCKPIT_DARK;
    ctx.fillRect(0, 0, 130, HEIGHT);
    ctx.fillRect(WIDTH - 130, 0, 130, HEIGHT);
    ctx.strokeStyle = COLORS.COCKPIT_MID;
    ctx.lineWidth = 3;
    ctx.strokeRect(0, 0, 130, HEIGHT);
    ctx.strokeRect(WIDTH - 130, 0, 130, HEIGHT);

    // Top & Floor Panels
    ctx.fillStyle = COLORS.COCKPIT_BLUE;
    ctx.fillRect(0, 0, WIDTH, 58);
    ctx.fillStyle = COLORS.COCKPIT_DARK;
    ctx.fillRect(0, HEIGHT - 52, WIDTH, 52);

    // Bunting ("HAPPY BIRTHDAY!")
    const letters = "HAPPYBIRTHDAY!".split('');
    const xStart = 140, xEnd = WIDTH - 140;
    const fw = (xEnd - xStart) / (letters.length - 1);
    letters.forEach((l, i) => {
      const fx = xStart + fw * i;
      const sag = Math.sin((Math.PI * (i + 1)) / (letters.length + 1)) * 16;
      const fy = 66 + sag;
      ctx.fillStyle = bColors[i % bColors.length];
      ctx.beginPath();
      ctx.moveTo(fx - 11, fy);
      ctx.lineTo(fx + 11, fy);
      ctx.lineTo(fx, fy + 26);
      ctx.closePath();
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(l, fx, fy + 14);
    });

    // Confetti
    confetti.forEach(c => {
      ctx.fillStyle = c.color;
      ctx.fillRect(c.x, c.y, c.sz, c.sz * 1.8);
    });

    // Items
    items.forEach(item => {
      ctx.save();
      ctx.translate(item.x, item.y);
      ctx.rotate(item.rot);
      ctx.font = '28px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(item.emoji, 0, 0);
      ctx.restore();
    });

    // Player
    if (state === 'PLAYING' || state === 'STAGE_CLEAR' || state === 'PAUSED') {
      const flicker = player.invincible > 0 && Math.floor(player.invincible * 12) % 2 === 0;
      if (!flicker) {
        ctx.save();
        const bob = Math.sin(player.walkTime) * 3;
        const px = player.x;
        const py = player.y + bob;

        // Baker Girl Sprite
        // Tray
        ctx.fillStyle = '#b0b8c8';
        ctx.fillRect(px - 35, py - 50 - 4, 70, 8);
        ctx.strokeStyle = '#ffffff';
        ctx.strokeRect(px - 35, py - 50 - 4, 70, 8);

        // Raised arms
        ctx.strokeStyle = '#dca064';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(px - 14, py - 15);
        ctx.lineTo(px - 22, py - 46);
        ctx.moveTo(px + 14, py - 15);
        ctx.lineTo(px + 22, py - 46);
        ctx.stroke();

        // Body / Golden top
        ctx.fillStyle = '#dcbe64';
        ctx.fillRect(px - 16, py - 16, 32, 28);
        // Belt
        ctx.fillStyle = '#371c08';
        ctx.fillRect(px - 16, py + 8, 32, 5);

        // Jeans
        ctx.fillStyle = '#466eb4';
        ctx.fillRect(px - 16, py + 13, 14, 26);
        ctx.fillRect(px + 2, py + 13, 14, 26);

        // Sneakers
        ctx.fillStyle = COLORS.ORANGE;
        ctx.fillRect(px - 18, py + 39, 14, 8);
        ctx.fillRect(px + 4, py + 39, 14, 8);

        // Head & Hair
        ctx.fillStyle = '#110d18'; // Dark wavy hair
        ctx.beginPath();
        ctx.arc(px, py - 26, 17, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffdca8'; // Face
        ctx.beginPath();
        ctx.arc(px, py - 24, 12, 0, Math.PI * 2);
        ctx.fill();

        // Eyes
        ctx.fillStyle = '#20150a';
        ctx.fillRect(px - 6, py - 26, 3, 3);
        ctx.fillRect(px + 3, py - 26, 3, 3);

        // Butterfly clip
        ctx.fillStyle = COLORS.PINK;
        ctx.fillRect(px + 4, py - 34, 5, 5);

        // Party hat
        ctx.fillStyle = COLORS.CYAN;
        ctx.beginPath();
        ctx.moveTo(px - 7, py - 36);
        ctx.lineTo(px + 7, py - 36);
        ctx.lineTo(px, py - 54);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
      }
    }

    // Particles
    particles.forEach(p => {
      ctx.save();
      const alpha = Math.max(0, p.life / p.maxLife);
      if (p.isText) {
        ctx.fillStyle = p.color;
        ctx.font = 'bold 20px monospace';
        ctx.textAlign = 'center';
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

    // Top HUD
    ctx.fillStyle = COLORS.GOLD;
    ctx.font = 'bold 22px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`SCORE: ${String(score).padStart(6, '0')}`, 20, 36);
    ctx.textAlign = 'center';
    ctx.fillText(`HI-SCORE: ${String(hiScore).padStart(6, '0')}`, WIDTH / 2, 36);

    // Timer Box
    const secs = Math.max(0, Math.ceil(timeLeft));
    const tStr = `0:${String(secs).padStart(2, '0')}`;
    ctx.fillStyle = timeLeft < 10 && Math.floor(globalTime * 4) % 2 === 0 ? COLORS.RED : COLORS.WHITE;
    ctx.font = 'bold 24px monospace';
    ctx.fillText(tStr, WIDTH / 2 + 180, 36);

    // Lives
    ctx.textAlign = 'right';
    let heartStr = '';
    for (let i = 0; i < MAX_LIVES; i++) heartStr += (i < lives ? '❤️ ' : '🖤 ');
    ctx.font = '20px sans-serif';
    ctx.fillText(heartStr, WIDTH - 20, 36);

    // Bottom HUD
    ctx.fillStyle = COLORS.CYAN;
    ctx.font = 'bold 20px monospace';
    ctx.textAlign = 'center';
    ctx.fillText("ZERO-G MODE", WIDTH / 2, HEIGHT - 20);
    ctx.fillStyle = COLORS.GOLD;
    ctx.textAlign = 'right';
    ctx.fillText(`STAGE ${stage}/${TOTAL_STAGES}`, WIDTH - 30, HEIGHT - 20);

    // Overlays
    if (state === 'MENU') {
      ctx.fillStyle = 'rgba(15, 10, 45, 0.88)';
      ctx.fillRect(WIDTH / 2 - 360, HEIGHT / 2 - 180, 720, 360);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 3;
      ctx.strokeRect(WIDTH / 2 - 360, HEIGHT / 2 - 180, 720, 360);

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = 'bold 46px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("ANTI-GRAVITY", WIDTH / 2, HEIGHT / 2 - 80);
      ctx.fillStyle = COLORS.PINK;
      ctx.font = 'bold 36px monospace';
      ctx.fillText("BIRTHDAY BAKE-OFF!", WIDTH / 2, HEIGHT / 2 - 25);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '18px monospace';
      ctx.fillText("Catch falling cake pieces — dodge the obstacles!", WIDTH / 2, HEIGHT / 2 + 30);

      if (Math.floor(globalTime * 2.5) % 2 === 0) {
        ctx.fillStyle = COLORS.CYAN;
        ctx.font = 'bold 24px monospace';
        ctx.fillText("PRESS SPACE OR TAP TO START", WIDTH / 2, HEIGHT / 2 + 85);
      }

      ctx.fillStyle = '#a0b0d0';
      ctx.font = '16px monospace';
      ctx.fillText("← → / A D MOVE    ESC PAUSE", WIDTH / 2, HEIGHT / 2 + 130);
    } else if (state === 'PAUSED') {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.WHITE;
      ctx.font = 'bold 50px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("— PAUSED —", WIDTH / 2, HEIGHT / 2 - 20);
      ctx.fillStyle = COLORS.CYAN;
      ctx.font = '22px monospace';
      ctx.fillText("Press ESC to Resume • Q to Quit", WIDTH / 2, HEIGHT / 2 + 40);
    } else if (state === 'STAGE_CLEAR') {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = 'bold 52px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`STAGE ${stage} CLEAR!`, WIDTH / 2, HEIGHT / 2 - 20);
      ctx.fillStyle = COLORS.CYAN;
      ctx.font = '26px monospace';
      ctx.fillText("GET READY...", WIDTH / 2, HEIGHT / 2 + 40);
    } else if (state === 'GAME_OVER') {
      ctx.fillStyle = 'rgba(50, 5, 5, 0.88)';
      ctx.fillRect(WIDTH / 2 - 320, HEIGHT / 2 - 160, 640, 320);
      ctx.strokeStyle = COLORS.RED;
      ctx.lineWidth = 3;
      ctx.strokeRect(WIDTH / 2 - 320, HEIGHT / 2 - 160, 640, 320);

      ctx.fillStyle = COLORS.RED;
      ctx.font = 'bold 44px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("CAKE DISASTER!", WIDTH / 2, HEIGHT / 2 - 80);
      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '22px monospace';
      ctx.fillText(`Score: ${score.toLocaleString()}`, WIDTH / 2, HEIGHT / 2 - 20);
      ctx.fillStyle = COLORS.GOLD;
      ctx.fillText(`Hi-Score: ${hiScore.toLocaleString()}`, WIDTH / 2, HEIGHT / 2 + 20);

      ctx.fillStyle = COLORS.CYAN;
      ctx.font = 'bold 22px monospace';
      ctx.fillText("PRESS SPACE TO RETRY", WIDTH / 2, HEIGHT / 2 + 80);
    } else if (state === 'WIN') {
      ctx.fillStyle = 'rgba(30, 25, 5, 0.88)';
      ctx.fillRect(WIDTH / 2 - 350, HEIGHT / 2 - 170, 700, 340);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 3;
      ctx.strokeRect(WIDTH / 2 - 350, HEIGHT / 2 - 170, 700, 340);

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = 'bold 40px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("🎂 BAKE-OFF CHAMPION! 🎂", WIDTH / 2, HEIGHT / 2 - 80);
      ctx.fillStyle = COLORS.PINK;
      ctx.font = '22px monospace';
      ctx.fillText("All 10 Zero-G Stages Conquered!", WIDTH / 2, HEIGHT / 2 - 25);
      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '26px monospace';
      ctx.fillText(`Final Score: ${score.toLocaleString()}`, WIDTH / 2, HEIGHT / 2 + 25);

      ctx.fillStyle = COLORS.CYAN;
      ctx.font = 'bold 22px monospace';
      ctx.fillText("PRESS SPACE TO PLAY AGAIN", WIDTH / 2, HEIGHT / 2 + 85);
    }

    ctx.restore();
  }

  // Animation Loop
  function loop(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;
    update(dt);
    draw();
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""

def handle_request(path: str = "/"):
    """Handle web HTTP request."""
    if path in ("/favicon.ico", "/favicon.png"):
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🎂</text></svg>'
        return svg.encode("utf-8"), "image/svg+xml"
    return HTML_CONTENT.encode("utf-8"), "text/html; charset=utf-8"


def app(environ, start_response):
    """
    Standard WSGI Application callable(environ, start_response).
    Fully compatible with Vercel Python runtime, Gunicorn, uWSGI, and wsgiref.
    """
    path = environ.get("PATH_INFO", "/")
    body, content_type = handle_request(path)
    start_response("200 OK", [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
    ])
    return [body]


application = app


def handler(event, context=None):
    """Serverless AWS Lambda / Vercel entrypoint."""
    path = "/"
    if isinstance(event, dict):
        path = event.get("rawPath") or event.get("path") or "/"
    body, content_type = handle_request(path)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": content_type,
            "Content-Length": str(len(body)),
        },
        "body": body.decode("utf-8", errors="replace"),
    }

