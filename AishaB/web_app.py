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
<title>Aisha's Birthday Bake-Off 🎂</title>
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

  // Aisha Head Avatar Image
  const aishaImg = new Image();
  aishaImg.src = "data:image/png;base64,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";

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

        // Aisha's Head Photo Attachment
        if (aishaImg.complete && aishaImg.naturalWidth > 0) {
          ctx.drawImage(aishaImg, px - 22, py - 52, 44, 48);
        } else {
          ctx.fillStyle = '#110d18';
          ctx.beginPath();
          ctx.arc(px, py - 26, 17, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#ffdca8';
          ctx.beginPath();
          ctx.arc(px, py - 24, 12, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#20150a';
          ctx.fillRect(px - 6, py - 26, 3, 3);
          ctx.fillRect(px + 3, py - 26, 3, 3);
          ctx.fillStyle = COLORS.PINK;
          ctx.fillRect(px + 4, py - 34, 5, 5);
        }

        // Party hat on top of hair
        ctx.fillStyle = COLORS.PINK;
        ctx.beginPath();
        ctx.moveTo(px - 8, py - 50);
        ctx.lineTo(px + 10, py - 50);
        ctx.lineTo(px + 1, py - 68);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = COLORS.WHITE;
        ctx.beginPath();
        ctx.arc(px + 1, py - 69, 3.5, 0, Math.PI * 2);
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
      ctx.fillStyle = 'rgba(15, 10, 45, 0.90)';
      ctx.fillRect(WIDTH / 2 - 360, HEIGHT / 2 - 200, 720, 400);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 3;
      ctx.strokeRect(WIDTH / 2 - 360, HEIGHT / 2 - 200, 720, 400);

      if (aishaImg.complete && aishaImg.naturalWidth > 0) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(WIDTH / 2, HEIGHT / 2 - 135, 32, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(aishaImg, WIDTH / 2 - 32, HEIGHT / 2 - 167, 64, 70);
        ctx.restore();
        ctx.strokeStyle = COLORS.GOLD;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(WIDTH / 2, HEIGHT / 2 - 135, 32, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = 'bold 46px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("AISHA'S", WIDTH / 2, HEIGHT / 2 - 80);
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
      ctx.fillStyle = 'rgba(30, 25, 5, 0.90)';
      ctx.fillRect(WIDTH / 2 - 350, HEIGHT / 2 - 190, 700, 370);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 3;
      ctx.strokeRect(WIDTH / 2 - 350, HEIGHT / 2 - 190, 700, 370);

      if (aishaImg.complete && aishaImg.naturalWidth > 0) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(WIDTH / 2, HEIGHT / 2 - 130, 34, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(aishaImg, WIDTH / 2 - 34, HEIGHT / 2 - 164, 68, 74);
        ctx.restore();
        ctx.strokeStyle = COLORS.GOLD;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(WIDTH / 2, HEIGHT / 2 - 130, 34, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = 'bold 36px monospace';
      ctx.textAlign = 'center';
      ctx.fillText("🎂 AISHA'S BAKE-OFF CHAMPION! 🎂", WIDTH / 2, HEIGHT / 2 - 80);
      ctx.fillStyle = COLORS.PINK;
      ctx.font = '22px monospace';
      ctx.fillText("Happy Birthday Aisha — All 10 Stages Conquered!", WIDTH / 2, HEIGHT / 2 - 25);
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

