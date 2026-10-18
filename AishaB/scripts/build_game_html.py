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
  #mute-btn {
    top: max(14px, env(safe-area-inset-top));
    left: calc(max(14px, env(safe-area-inset-left)) + 46px);
    font-size: 16px;
  }
  #crt-btn {
    top: max(14px, env(safe-area-inset-top));
    left: calc(max(14px, env(safe-area-inset-left)) + 92px);
    font-size: 16px;
  }
  /* CRT Arcade Cabinet Bezel */
  .arcade-bezel {
    display: none;
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 15;
    box-shadow: inset 0 0 100px rgba(0, 0, 0, 0.92), inset 0 0 35px rgba(0, 220, 255, 0.4);
    border: 10px solid #08031a;
    border-radius: 20px;
  }
  .arcade-bezel.active {
    display: block;
  }
  .arcade-marquee {
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 8px;
    letter-spacing: 2px;
    color: #ffd700;
    text-shadow: 0 0 8px #ff4da6, 0 0 16px #00dcff;
    white-space: nowrap;
    opacity: 0.95;
    pointer-events: none;
    z-index: 16;
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

  /* Action buttons (START / RESUME / SHARE / MIC) at bottom center for menus & ceremonies */
  .action-zone {
    position: absolute;
    bottom: max(16px, env(safe-area-inset-bottom));
    left: 50%;
    transform: translateX(-50%);
    pointer-events: auto;
    z-index: 22;
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    max-width: 92vw;
  }
  .btn-action {
    width: auto;
    min-width: 130px;
    height: 46px;
    padding: 0 20px;
    border-radius: 24px;
    font-size: 11px;
    letter-spacing: 1.2px;
    border-color: #ffd700;
    color: #ffd700;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6), 0 0 16px rgba(255, 215, 0, 0.4), inset 0 0 10px rgba(255, 215, 0, 0.25);
  }
  .btn-action:active, .btn-action.active {
    background: rgba(255, 215, 0, 0.4);
    box-shadow: 0 0 26px rgba(255, 215, 0, 0.85), inset 0 0 14px #ffffff;
    color: #ffffff;
  }
  .btn-resume {
    border-color: #00dcff;
    color: #00dcff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6), 0 0 16px rgba(0, 220, 255, 0.4), inset 0 0 10px rgba(0, 220, 255, 0.25);
  }
  .btn-resume:active, .btn-resume.active {
    background: rgba(0, 220, 255, 0.4);
    box-shadow: 0 0 26px rgba(0, 220, 255, 0.85), inset 0 0 14px #ffffff;
    color: #ffffff;
  }
  .btn-share {
    border-color: #ff6ebe;
    color: #ff6ebe;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6), 0 0 16px rgba(255, 110, 190, 0.4), inset 0 0 10px rgba(255, 110, 190, 0.25);
  }
  .btn-share:active, .btn-share.active {
    background: rgba(255, 110, 190, 0.4);
    box-shadow: 0 0 26px rgba(255, 110, 190, 0.85), inset 0 0 14px #ffffff;
    color: #ffffff;
  }
  .btn-mic {
    border-color: #37be46;
    color: #37be46;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6), 0 0 16px rgba(55, 190, 70, 0.4), inset 0 0 10px rgba(55, 190, 70, 0.25);
  }
  .btn-mic.active {
    background: rgba(55, 190, 70, 0.5);
    color: #ffffff;
    box-shadow: 0 0 26px rgba(55, 190, 70, 0.9), inset 0 0 14px #ffffff;
  }
  /* Shareable Victory Polaroid Certificate Modal */
  #polaroid-modal {
    display: none;
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    background: rgba(6, 3, 18, 0.92);
    z-index: 100;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 16px;
    box-sizing: border-box;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  #polaroid-wrap {
    max-width: 90vw;
    max-height: 82dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  #polaroid-img {
    max-width: 100%;
    max-height: 68dvh;
    border-radius: 8px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9), 0 0 24px rgba(255, 215, 0, 0.35);
    display: block;
  }
  .modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 14px;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
  }
  .modal-btn {
    background: #ff4da6;
    color: #fff;
    border: 2px solid #fff;
    padding: 10px 20px;
    border-radius: 20px;
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(255, 77, 166, 0.5);
  }
  .modal-btn-close {
    background: #374682;
    border-color: #00dcff;
    color: #00dcff;
  }
</style>
</head>
<body>

<div id="game-wrap">
  <div class="scanlines"></div>
  <canvas id="gameCanvas"></canvas>
  <div class="arcade-bezel" id="arcade-bezel">
    <div class="arcade-marquee">★ AISHA'S SPACE BAKERY ★</div>
  </div>
  <button class="hud-btn" id="fs-btn" title="Toggle Fullscreen">⛶</button>
  <button class="hud-btn" id="mute-btn" title="Toggle Sound">🔊</button>
  <button class="hud-btn" id="crt-btn" title="Toggle CRT Arcade Cabinet Mode">📺</button>
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
      <button class="control-btn btn-action btn-resume" id="btn-resume" style="display:none;">★ RESUME ★</button>
      <button class="control-btn btn-action btn-share" id="btn-share" style="display:none;">📸 POLAROID</button>
      <button class="control-btn btn-action btn-mic" id="btn-mic" style="display:none;">🎤 BLOW MIC</button>
    </div>
  </div>
  <div id="polaroid-modal">
    <div id="polaroid-wrap">
      <img id="polaroid-img" alt="Aisha Polaroid Certificate" />
      <p style="font-size: 9px; color: #ffd700; margin-top: 10px; text-align: center; text-shadow: 0 0 8px #000;">★ TAP &amp; HOLD IMAGE TO SAVE TO PHOTOS ★</p>
      <div class="modal-actions">
        <button class="modal-btn" id="modal-download-btn">DOWNLOAD 📥</button>
        <button class="modal-btn modal-btn-close" id="modal-close-btn">CLOSE ✕</button>
      </div>
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
  let bgmMuted = localStorage.getItem('anti_grav_muted') === 'true';
  let bgmGain = null;
  let bgmInterval = null;
  let bgmStep = 0;

  // Upbeat 8-bit chiptune bakery melody & bass (with Happy Birthday phrase woven in!)
  const MELODY_NOTES = [
    523, 0, 523, 587, 523, 659, 587, 0,
    523, 0, 523, 587, 523, 784, 659, 0,
    523, 0, 523, 1046, 880, 659, 587, 523,
    988, 0, 988, 880, 659, 784, 659, 0
  ];
  const BASS_NOTES = [
    130.8, 0, 196.0, 130.8, 174.6, 0, 130.8, 196.0,
    146.8, 0, 220.0, 146.8, 130.8, 0, 196.0, 130.8,
    174.6, 0, 220.0, 174.6, 130.8, 0, 196.0, 130.8,
    196.0, 0, 246.9, 196.0, 130.8, 0, 196.0, 130.8
  ];

  function startBgm() {
    if (bgmInterval || !audioCtx) return;
    try {
      bgmGain = audioCtx.createGain();
      bgmGain.gain.setValueAtTime(bgmMuted ? 0.0001 : 0.045, audioCtx.currentTime);
      bgmGain.connect(audioCtx.destination);

      bgmInterval = setInterval(() => {
        if (!audioCtx || audioCtx.state !== 'running') return;
        if (state === 'PAUSED' || state === 'GAME_OVER') return;

        const mFreq = MELODY_NOTES[bgmStep % MELODY_NOTES.length];
        const bFreq = BASS_NOTES[bgmStep % BASS_NOTES.length];
        bgmStep++;

        // Lead chiptune square wave
        if (mFreq > 0 && !bgmMuted) {
          try {
            const osc = audioCtx.createOscillator();
            const noteGain = audioCtx.createGain();
            osc.type = 'square';
            osc.frequency.setValueAtTime(mFreq, audioCtx.currentTime);
            noteGain.gain.setValueAtTime(0.04, audioCtx.currentTime);
            noteGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.11);
            osc.connect(noteGain);
            noteGain.connect(bgmGain);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.11);
          } catch(e) {}
        }

        // Bass triangle wave
        if (bFreq > 0 && !bgmMuted) {
          try {
            const bOsc = audioCtx.createOscillator();
            const bGain = audioCtx.createGain();
            bOsc.type = 'triangle';
            bOsc.frequency.setValueAtTime(bFreq, audioCtx.currentTime);
            bGain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            bGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.13);
            bOsc.connect(bGain);
            bGain.connect(bgmGain);
            bOsc.start();
            bOsc.stop(audioCtx.currentTime + 0.13);
          } catch(e) {}
        }
      }, 140);
    } catch(e) {}
  }

  function setMuted(muted) {
    bgmMuted = muted;
    localStorage.setItem('anti_grav_muted', bgmMuted);
    const muteBtn = document.getElementById('mute-btn');
    if (muteBtn) muteBtn.textContent = bgmMuted ? '🔇' : '🔊';
    if (bgmGain && audioCtx) {
      bgmGain.gain.setValueAtTime(bgmMuted ? 0.0001 : 0.045, audioCtx.currentTime);
    }
  }

  function initAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    startBgm();
  }
  ['touchstart', 'pointerdown', 'click', 'keydown'].forEach(ev => {
    window.addEventListener(ev, initAudio, { passive: true, once: false });
  });

  function playTone(freq, type, duration, gainVal=0.15) {
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
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
  function sfxBlow() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    try {
      const bufferSize = audioCtx.sampleRate * 0.25;
      const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
      }
      const noise = audioCtx.createBufferSource();
      noise.buffer = buffer;
      const filter = audioCtx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.value = 750;
      const gain = audioCtx.createGain();
      gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.25);
      noise.connect(filter);
      filter.connect(gain);
      gain.connect(audioCtx.destination);
      noise.start();
    } catch(e) {}
  }
  function sfxPowerup() {
    initAudio();
    if (bgmMuted) return;
    [440, 554, 659, 880].forEach((f, i) => {
      setTimeout(() => playTone(f, 'sine', 0.12, 0.18), i * 50);
    });
  }
  function sfxCombo() {
    initAudio();
    if (bgmMuted) return;
    playTone(880, 'triangle', 0.12, 0.2);
    setTimeout(() => playTone(1174, 'triangle', 0.16, 0.22), 60);
  }

  // Full 8-Bit Happy Birthday to You Chiptune
  function stopHappyBirthdaySong() {
    hbTimeoutIds.forEach(id => clearTimeout(id));
    hbTimeoutIds = [];
    isPlayingHappyBirthday = false;
    if (bgmGain && audioCtx) {
      bgmGain.gain.setValueAtTime(bgmMuted ? 0.0001 : 0.045, audioCtx.currentTime);
    }
  }

  function playHappyBirthdaySong() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;

    stopHappyBirthdaySong();
    isPlayingHappyBirthday = true;

    // Duck background BGM while birthday anthem plays
    if (bgmGain) {
      bgmGain.gain.setValueAtTime(0.0001, audioCtx.currentTime);
    }

    const notes = [
      // Phrase 1: "Happy Birthday to you"
      { f: 392, d: 0.28, bass: 196 },
      { f: 392, d: 0.20, bass: 0 },
      { f: 440, d: 0.48, bass: 220 },
      { f: 392, d: 0.48, bass: 196 },
      { f: 523, d: 0.48, bass: 261 },
      { f: 494, d: 0.85, bass: 247 },
      { f: 0,   d: 0.18, bass: 0 },

      // Phrase 2: "Happy Birthday to you"
      { f: 392, d: 0.28, bass: 196 },
      { f: 392, d: 0.20, bass: 0 },
      { f: 440, d: 0.48, bass: 220 },
      { f: 392, d: 0.48, bass: 196 },
      { f: 587, d: 0.48, bass: 294 },
      { f: 523, d: 0.85, bass: 261 },
      { f: 0,   d: 0.18, bass: 0 },

      // Phrase 3: "Happy Birthday dear Aisha"
      { f: 392, d: 0.28, bass: 196 },
      { f: 392, d: 0.20, bass: 0 },
      { f: 784, d: 0.52, bass: 392 },
      { f: 659, d: 0.52, bass: 330 },
      { f: 523, d: 0.52, bass: 261 },
      { f: 494, d: 0.52, bass: 247 },
      { f: 440, d: 0.78, bass: 220 },
      { f: 0,   d: 0.18, bass: 0 },

      // Phrase 4: "Happy Birthday to you!"
      { f: 698, d: 0.28, bass: 349 },
      { f: 698, d: 0.20, bass: 0 },
      { f: 659, d: 0.52, bass: 330 },
      { f: 523, d: 0.52, bass: 261 },
      { f: 587, d: 0.52, bass: 294 },
      { f: 523, d: 1.15, bass: 261 }
    ];

    let tAccum = 0;
    notes.forEach(n => {
      const tid = setTimeout(() => {
        if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
        if (n.f > 0) {
          try {
            // Square wave lead with bright retro pulse
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'square';
            osc.frequency.setValueAtTime(n.f, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + n.d);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + n.d);

            // Triangle wave bass
            if (n.bass > 0) {
              const bOsc = audioCtx.createOscillator();
              const bGain = audioCtx.createGain();
              bOsc.type = 'triangle';
              bOsc.frequency.setValueAtTime(n.bass / 2, audioCtx.currentTime);
              bGain.gain.setValueAtTime(0.12, audioCtx.currentTime);
              bGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + n.d);
              bOsc.connect(bGain);
              bGain.connect(audioCtx.destination);
              bOsc.start();
              bOsc.stop(audioCtx.currentTime + n.d);
            }
          } catch(e) {}
        }
      }, tAccum * 1000);
      hbTimeoutIds.push(tid);
      tAccum += n.d;
    });

    const finishTid = setTimeout(() => {
      stopHappyBirthdaySong();
    }, tAccum * 1000 + 400);
    hbTimeoutIds.push(finishTid);
  }

  // Real Microphone Breath Detection
  async function toggleMic() {
    if (micEnabled) {
      stopMic();
    } else {
      await startMic();
    }
    syncUIState();
  }

  async function startMic() {
    initAudio();
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert("Microphone is not supported on this browser.");
      return;
    }
    try {
      micStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') await audioCtx.resume();

      const source = audioCtx.createMediaStreamSource(micStream);
      micAnalyser = audioCtx.createAnalyser();
      micAnalyser.fftSize = 256;
      micAnalyser.smoothingTimeConstant = 0.25;
      source.connect(micAnalyser);
      micDataArray = new Uint8Array(micAnalyser.frequencyBinCount);
      micEnabled = true;
      haptic(30);
    } catch (err) {
      console.warn("Microphone access error:", err);
      micEnabled = false;
      alert("Microphone permission was not granted. Tap candles to blow them out!");
    }
  }

  function stopMic() {
    if (micStream) {
      try {
        micStream.getTracks().forEach(track => track.stop());
      } catch(e) {}
      micStream = null;
    }
    micAnalyser = null;
    micDataArray = null;
    micEnabled = false;
    micBlowLevel = 0;
    micBlowFrames = 0;
  }

  // Shareable Victory Polaroid Certificate Generator
  function generatePolaroidCanvas() {
    const cw = 700;
    const ch = 920;
    const pCanvas = document.createElement('canvas');
    pCanvas.width = cw;
    pCanvas.height = ch;
    const pCtx = pCanvas.getContext('2d');

    // Cosmic space table backdrop
    const bgGrad = pCtx.createRadialGradient(cw / 2, ch / 2, 50, cw / 2, ch / 2, cw * 0.8);
    bgGrad.addColorStop(0, '#1c1444');
    bgGrad.addColorStop(1, '#090518');
    pCtx.fillStyle = bgGrad;
    pCtx.fillRect(0, 0, cw, ch);

    // Polaroid Outer Card
    const pad = 36;
    const cardW = cw - pad * 2;
    const cardH = ch - pad * 2;
    pCtx.fillStyle = '#faf8f5';
    pCtx.shadowColor = 'rgba(0, 0, 0, 0.7)';
    pCtx.shadowBlur = 35;
    pCtx.shadowOffsetY = 15;
    if (pCtx.roundRect) pCtx.roundRect(pad, pad, cardW, cardH, 8);
    else pCtx.rect(pad, pad, cardW, cardH);
    pCtx.fill();
    pCtx.shadowBlur = 0;
    pCtx.shadowOffsetY = 0;

    // Polaroid Card Header
    pCtx.fillStyle = '#ff4da6';
    pCtx.font = 'bold 15px "Press Start 2P", sans-serif';
    pCtx.textAlign = 'center';
    pCtx.fillText("★ AISHA'S BIRTHDAY BAKE-OFF ★", cw / 2, pad + 38);

    pCtx.fillStyle = '#4a5568';
    pCtx.font = 'bold 9px "Press Start 2P", sans-serif';
    pCtx.fillText("OFFICIAL COSMIC BAKER CERTIFICATE", cw / 2, pad + 58);

    // Photo Cutout Frame
    const photoX = pad + 24;
    const photoY = pad + 75;
    const photoW = cardW - 48;
    const photoH = 500;
    pCtx.fillStyle = '#0f0826';
    pCtx.fillRect(photoX, photoY, photoW, photoH);

    // Photo Cosmic Nebula
    const photoGrad = pCtx.createRadialGradient(photoX + photoW / 2, photoY + photoH / 2, 20, photoX + photoW / 2, photoY + photoH / 2, photoW * 0.7);
    photoGrad.addColorStop(0, '#2d1b58');
    photoGrad.addColorStop(1, '#080415');
    pCtx.fillStyle = photoGrad;
    pCtx.fillRect(photoX, photoY, photoW, photoH);

    // Stardust Sparkles in photo background
    const pColors = ['#ffd700', '#00dcff', '#ff6ebe', '#37be46', '#ffffff'];
    for (let i = 0; i < 40; i++) {
      pCtx.fillStyle = pColors[i % pColors.length];
      const sx = photoX + 20 + ((i * 47) % (photoW - 40));
      const sy = photoY + 20 + ((i * 31) % (photoH - 40));
      pCtx.fillRect(sx, sy, 3, 3);
    }

    // Centered Aisha Portrait
    const imgW = 280;
    const imgH = 370;
    const imgX = photoX + (photoW - imgW) / 2;
    const imgY = photoY + (photoH - imgH) / 2 + 20;

    pCtx.save();
    pCtx.strokeStyle = '#ffd700';
    pCtx.lineWidth = 4;
    pCtx.strokeRect(imgX - 2, imgY - 2, imgW + 4, imgH + 4);

    if (aishaPortrait.complete && aishaPortrait.naturalWidth > 0) {
      pCtx.drawImage(aishaPortrait, imgX, imgY, imgW, imgH);
    } else if (aishaHead.complete && aishaHead.naturalWidth > 0) {
      pCtx.drawImage(aishaHead, imgX, imgY, imgW, imgH);
    }
    pCtx.restore();

    // Golden Birthday Tiara & Crown atop Aisha's head in portrait
    const crownCenterX = imgX + imgW / 2;
    const crownTopY = imgY - 14;
    pCtx.save();
    pCtx.translate(crownCenterX, crownTopY);
    pCtx.scale(2.2, 2.2);
    pCtx.fillStyle = '#ffd700';
    pCtx.beginPath();
    pCtx.moveTo(-16, 4);
    pCtx.lineTo(-16, -10);
    pCtx.lineTo(-8, -4);
    pCtx.lineTo(0, -18);
    pCtx.lineTo(8, -4);
    pCtx.lineTo(16, -10);
    pCtx.lineTo(16, 4);
    pCtx.closePath();
    pCtx.fill();
    pCtx.strokeStyle = '#ffffff';
    pCtx.lineWidth = 1.2;
    pCtx.stroke();
    pCtx.fillStyle = '#ff1155';
    pCtx.fillRect(-2, -6, 4, 4);
    pCtx.fillStyle = '#00dcff';
    pCtx.fillRect(-10, -3, 3, 3);
    pCtx.fillRect(7, -3, 3, 3);
    pCtx.restore();

    // Photo inner border
    pCtx.strokeStyle = '#d2d6dc';
    pCtx.lineWidth = 2;
    pCtx.strokeRect(photoX, photoY, photoW, photoH);

    // Polaroid Bottom Margin
    const marginY = photoY + photoH + 28;

    // Gold Certified Master Baker Seal with Satin Ribbon
    const sealX = photoX + photoW - 70;
    const sealY = marginY + 68;
    pCtx.save();
    pCtx.fillStyle = '#ffd700';
    pCtx.shadowColor = 'rgba(218, 165, 32, 0.4)';
    pCtx.shadowBlur = 12;
    pCtx.beginPath();
    pCtx.arc(sealX, sealY, 36, 0, Math.PI * 2);
    pCtx.fill();
    pCtx.strokeStyle = '#b8860b';
    pCtx.lineWidth = 3;
    pCtx.stroke();

    pCtx.fillStyle = '#e6005c';
    pCtx.beginPath();
    pCtx.moveTo(sealX - 14, sealY + 28);
    pCtx.lineTo(sealX - 22, sealY + 70);
    pCtx.lineTo(sealX - 10, sealY + 60);
    pCtx.lineTo(sealX, sealY + 70);
    pCtx.lineTo(sealX - 4, sealY + 28);
    pCtx.fill();
    pCtx.beginPath();
    pCtx.moveTo(sealX + 4, sealY + 28);
    pCtx.lineTo(sealX, sealY + 70);
    pCtx.lineTo(sealX + 10, sealY + 60);
    pCtx.lineTo(sealX + 22, sealY + 70);
    pCtx.lineTo(sealX + 14, sealY + 28);
    pCtx.fill();

    pCtx.fillStyle = '#000000';
    pCtx.font = 'bold 7px sans-serif';
    pCtx.textAlign = 'center';
    pCtx.fillText("★ CERTIFIED ★", sealX, sealY - 8);
    pCtx.fillText("MASTER", sealX, sealY + 2);
    pCtx.fillText("BAKER 👑", sealX, sealY + 12);
    pCtx.restore();

    // Handwritten Birthday Message & Stats
    pCtx.fillStyle = '#1a202c';
    pCtx.font = 'bold 22px "Press Start 2P", cursive, sans-serif';
    pCtx.textAlign = 'left';
    pCtx.fillText("HAPPY BIRTHDAY AISHA! 🎂", photoX, marginY + 12);

    pCtx.fillStyle = '#2b6cb0';
    pCtx.font = 'bold 12px "Press Start 2P", monospace';
    const stageTitle = (stage >= TOTAL_STAGES) ? "★ GRAND CHAMPION BAKER (ALL 30 LEVELS) ★" : `★ CERTIFIED COSMIC BAKER (STAGE ${stage}) ★`;
    pCtx.fillText(stageTitle, photoX, marginY + 45);

    pCtx.fillStyle = '#4a5568';
    pCtx.font = '11px "Press Start 2P", monospace';
    pCtx.fillText(`FINAL SCORE: ${score.toLocaleString()} PTS`, photoX, marginY + 78);
    pCtx.fillText("RANK: GALAXY QUEEN BAKER 👑", photoX, marginY + 102);

    const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    pCtx.fillStyle = '#a0aec0';
    pCtx.font = '9px "Press Start 2P", monospace';
    pCtx.fillText(`DATE: ${dateStr} • VERIFIED BIRTHDAY EDITION`, photoX, marginY + 134);

    return pCanvas;
  }

  let latestPolaroidBlob = null;
  function shareOrSavePolaroid() {
    initAudio();
    haptic([30, 40]);
    const pCanvas = generatePolaroidCanvas();
    pCanvas.toBlob(async (blob) => {
      if (!blob) return;
      latestPolaroidBlob = blob;
      const file = new File([blob], 'aisha-birthday-champion.png', { type: 'image/png' });

      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
          await navigator.share({
            title: "Aisha's Birthday Bake-Off 🎂",
            text: `Aisha conquered the Galaxy Bake-Off with ${score.toLocaleString()} points! Happy Birthday Aisha! 🎂👑`,
            files: [file]
          });
          return;
        } catch (err) {
          if (err.name !== 'AbortError') console.warn("Share failed, falling back to modal:", err);
        }
      }

      const url = URL.createObjectURL(blob);
      showPolaroidModal(url);
    }, 'image/png');
  }

  function showPolaroidModal(imgUrl) {
    const modal = document.getElementById('polaroid-modal');
    const img = document.getElementById('polaroid-img');
    if (modal && img) {
      img.src = imgUrl;
      modal.style.display = 'flex';
    }
  }

  function closePolaroidModal() {
    const modal = document.getElementById('polaroid-modal');
    if (modal) modal.style.display = 'none';
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
  const TOTAL_STAGES = 30;
  const ITEMS_PER_STAGE = 20;
  const STAGE_DURATION = 60;
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

  // Checkpoints
  let checkpointStage = parseInt(localStorage.getItem('anti_grav_checkpoint') || '0');
  let checkpointScore = parseInt(localStorage.getItem('anti_grav_checkpoint_score') || '0');

  // Real Microphone Breath Detection
  let micStream = null;
  let micAnalyser = null;
  let micDataArray = null;
  let micEnabled = false;
  let micBlowLevel = 0;
  let micBlowFrames = 0;

  // Full 8-Bit Happy Birthday Chiptune Player
  let isPlayingHappyBirthday = false;
  let hbTimeoutIds = [];
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
    walkTime: 0,
    vx: 0,
    prevX: 360,
    tilt: 0,
    happyTime: 0,
    worryTime: 0,
    traySquash: 1.0,
    traySquashVel: 0
  };

  // Graphics Overhaul FX Collections
  let ghostTrails = [];
  let candyComets = [];
  let cometTimer = 5.0;
  let crtMode = localStorage.getItem('anti_grav_crt') === 'true';

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
    if (state === 'MENU') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxY = HEIGHT / 2 - 265;
      if (checkpointStage > 1 && coords.y >= boxY + 410 && coords.y <= boxY + 455) {
        resumeCheckpoint();
      } else {
        startGame();
      }
      haptic(25);
      return;
    }
    if (state === 'GAME_OVER') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxY = HEIGHT / 2 - 265;
      if (checkpointStage > 1 && coords.y >= boxY + 410 && coords.y <= boxY + 455) {
        resumeCheckpoint();
      } else {
        startGame();
      }
      haptic(25);
      return;
    }
    if (state === 'WIN') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxY = HEIGHT / 2 - 265;
      if (coords.y >= boxY + 450 && coords.y <= boxY + 500) {
        shareOrSavePolaroid();
      } else {
        startGame();
      }
      haptic(25);
      return;
    }
    if (state === 'CANDLE_CEREMONY') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxY = HEIGHT / 2 - Math.min(HEIGHT - 80, 560) / 2;
      if (!ceremonyAllBlown && coords.y >= boxY + 490 && coords.y <= boxY + 530) {
        toggleMic();
        return;
      }
      if (ceremonyAllBlown && coords.y >= boxY + 460 && coords.y <= boxY + 510) {
        shareOrSavePolaroid();
        return;
      }
      blowCandles(coords.x, coords.y);
      return;
    }
    if (state === 'MILESTONE') {
      continueMilestone();
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
      else if (state === 'CANDLE_CEREMONY') blowCandles();
      else if (state === 'MILESTONE') continueMilestone();
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
  const btnResume = document.getElementById('btn-resume');
  const btnShare = document.getElementById('btn-share');
  const btnMic = document.getElementById('btn-mic');
  const actionZone = document.getElementById('action-zone');
  const btnPause = document.getElementById('pause-btn');
  const btnFS = document.getElementById('fs-btn');
  const btnMute = document.getElementById('mute-btn');
  const modalDownloadBtn = document.getElementById('modal-download-btn');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  if (btnMute) {
    btnMute.textContent = bgmMuted ? '🔇' : '🔊';
    btnMute.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      setMuted(!bgmMuted);
      haptic(20);
    });
  }

  const btnCRT = document.getElementById('crt-btn');
  const arcadeBezel = document.getElementById('arcade-bezel');
  if (btnCRT && arcadeBezel) {
    if (crtMode) arcadeBezel.classList.add('active');
    btnCRT.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      crtMode = !crtMode;
      localStorage.setItem('anti_grav_crt', crtMode);
      arcadeBezel.classList.toggle('active', crtMode);
      haptic(20);
    });
  }

  if (btnResume) {
    btnResume.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      haptic(25);
      resumeCheckpoint();
    });
  }
  if (btnShare) {
    btnShare.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      shareOrSavePolaroid();
    });
  }
  if (btnMic) {
    btnMic.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      toggleMic();
    });
  }
  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closePolaroidModal);
  }
  if (modalDownloadBtn) {
    modalDownloadBtn.addEventListener('click', () => {
      if (!latestPolaroidBlob) return;
      const url = URL.createObjectURL(latestPolaroidBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'aisha-birthday-champion.png';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      haptic(20);
    });
  }
  const polaroidModal = document.getElementById('polaroid-modal');
  if (polaroidModal) {
    polaroidModal.addEventListener('click', (e) => {
      if (e.target === polaroidModal) closePolaroidModal();
    });
  }

  function syncUIState() {
    checkpointStage = parseInt(localStorage.getItem('anti_grav_checkpoint') || '0');
    checkpointScore = parseInt(localStorage.getItem('anti_grav_checkpoint_score') || '0');

    if (actionZone) {
      if (state === 'PLAYING') {
        actionZone.style.display = 'none';
      } else {
        actionZone.style.display = 'flex';
      }
    }

    if (btnResume) {
      if ((state === 'MENU' || state === 'GAME_OVER') && checkpointStage > 1) {
        btnResume.style.display = 'block';
        btnResume.textContent = '★ RESUME (LVL ' + checkpointStage + ')';
      } else {
        btnResume.style.display = 'none';
      }
    }

    if (btnMic) {
      if (state === 'CANDLE_CEREMONY' && !ceremonyAllBlown) {
        btnMic.style.display = 'block';
        btnMic.classList.toggle('active', micEnabled);
        btnMic.textContent = micEnabled ? '🎤 MIC: LISTENING...' : '🎤 BLOW MIC';
      } else {
        btnMic.style.display = 'none';
      }
    }

    if (btnShare) {
      if (state === 'WIN' || (state === 'CANDLE_CEREMONY' && ceremonyAllBlown)) {
        btnShare.style.display = 'block';
        btnShare.textContent = '📸 SHARE POLAROID';
      } else {
        btnShare.style.display = 'none';
      }
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
    else if (state === 'CANDLE_CEREMONY') blowCandles();
    else if (state === 'MILESTONE') continueMilestone();
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
    CAKE: 50,
    STRAWBERRY: 50,
    CHERRY: 50,
    CANDLE: 50,
    CANDY: 50,
    FROSTING: 50
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

  // Items & Gameplay Enhancements
  let items = [];
  let spawnTimer = 0.5;
  let comboStreak = 0;
  let magnetTime = 0;
  let shieldActive = false;
  let slowmoTime = 0;
  let sugarRushCount = 0;
  let powerupSpawnTimer = 14;
  let hazardWarnings = [];

  // Interactive Candle Blowout Ceremony
  let ceremonyCandles = [];
  let ceremonyAllBlown = false;
  let ceremonySmokeParticles = [];

  const MILESTONE_MESSAGES = {
    5: {
      title: "★ SWEET START! ★",
      sub: "HAPPY BIRTHDAY AISHA! 🧁",
      note: "LEVEL 5 COMPLETE! THE GALAXY BAKERY IS HEATING UP!",
      bonus: "+1,000 WISH BONUS AWARDED"
    },
    10: {
      title: "★ CHAMPION BAKER! ★",
      sub: "HAPPY BIRTHDAY AISHA! 🍰",
      note: "10 LEVELS CONQUERED! AISHA IS 10X SWEETER TODAY!",
      bonus: "+1,000 CHAMPION BONUS AWARDED"
    },
    15: {
      title: "★ HALFWAY FEAST! ★",
      sub: "HAPPY BIRTHDAY AISHA! 🌟",
      note: "HALFWAY THROUGH SPACE! MAKE YOUR BIGGEST BIRTHDAY WISH!",
      bonus: "+1,000 WISH BONUS AWARDED"
    },
    20: {
      title: "★ GRAND PASTRY MASTER! ★",
      sub: "HAPPY BIRTHDAY AISHA! 🎂",
      note: "20 LEVELS DOWN! AISHA IS AN ABSOLUTE BAKING LEGEND!",
      bonus: "+1,000 MASTER BONUS AWARDED"
    },
    25: {
      title: "★ COSMIC CONFECTIONER! ★",
      sub: "HAPPY BIRTHDAY AISHA! 👑",
      note: "ONLY 5 LEVELS REMAIN! THE ULTIMATE BIRTHDAY CROWN AWAITS!",
      bonus: "+1,000 CROWN BONUS AWARDED"
    },
    30: {
      title: "★ GRAND CHAMPION BAKER! ★",
      sub: "HAPPY BIRTHDAY AISHA! 🎂🎉",
      note: "ALL 30 LEVELS CONQUERED! AISHA'S ULTIMATE BIRTHDAY WISH GRANTED!",
      bonus: "★ GALAXY BAKE-OFF COMPLETED! ★"
    }
  };

  function initCandleCeremony() {
    ceremonyAllBlown = false;
    ceremonySmokeParticles = [];
    ceremonyCandles = [];

    const cakeCenterY = HEIGHT / 2 + 75;
    const offsets = [-80, -40, 0, 40, 80];
    offsets.forEach((ox, idx) => {
      ceremonyCandles.push({
        id: idx,
        x: WIDTH / 2 + ox,
        y: cakeCenterY - 120,
        lit: true,
        flicker: Math.random() * 10,
        color: ['#ff4da6', '#00dcff', '#ffd700', '#ff9100', '#37be46'][idx % 5]
      });
    });

    btnAction.textContent = 'BLOW 🎂';
    haptic(40);
  }

  function blowCandles(tapX, tapY) {
    if (ceremonyAllBlown) {
      if (stage >= TOTAL_STAGES) {
        startGame();
      } else {
        continueMilestone();
      }
      return;
    }

    const litCandles = ceremonyCandles.filter(c => c.lit);
    if (litCandles.length > 0) {
      let targetCandles = [];
      if (tapX !== undefined && tapY !== undefined) {
        const sorted = [...litCandles].sort((a, b) => Math.hypot(a.x - tapX, a.y - tapY) - Math.hypot(b.x - tapX, b.y - tapY));
        if (Math.hypot(WIDTH / 2 - tapX, (HEIGHT / 2 + 30) - tapY) < 160) {
          targetCandles = litCandles;
        } else {
          targetCandles = sorted.slice(0, 2);
        }
      } else {
        targetCandles = litCandles.slice(0, 2);
      }

      targetCandles.forEach(c => {
        c.lit = false;
        for (let i = 0; i < 16; i++) {
          ceremonySmokeParticles.push({
            x: c.x + (Math.random() - 0.5) * 6,
            y: c.y - 25,
            vx: (Math.random() - 0.5) * 30,
            vy: -40 - Math.random() * 55,
            radius: 4 + Math.random() * 5,
            life: 1.1,
            maxLife: 1.1,
            alpha: 0.8
          });
        }
      });

      sfxBlow();
      haptic([25, 30]);

      if (ceremonyCandles.every(c => !c.lit)) {
        ceremonyAllBlown = true;
        score += 1000;
        if (score > hiScore) {
          hiScore = score;
          localStorage.setItem('anti_grav_hiscore', hiScore);
        }
        // Save Checkpoint for upcoming stage!
        if (stage < TOTAL_STAGES) {
          const nextCp = stage + 1;
          localStorage.setItem('anti_grav_checkpoint', nextCp);
          localStorage.setItem('anti_grav_checkpoint_score', score);
          checkpointStage = nextCp;
          checkpointScore = score;
        }
        stopMic();
        playHappyBirthdaySong();
        haptic([50, 40, 50, 40, 120]);
        for (let k = 0; k < 6; k++) {
          setTimeout(() => {
            addFireworks(120 + Math.random() * (WIDTH - 240), 140 + Math.random() * 220,
                         bColors[Math.floor(Math.random() * bColors.length)]);
          }, k * 180);
        }
        btnAction.textContent = (stage < TOTAL_STAGES) ? ('STAGE ' + (stage + 1) + ' ▶') : 'PLAY AGAIN ★';
        syncUIState();
      }
    }
  }

  function activatePowerup(type) {
    if (type === 'MAGNET') {
      magnetTime = 7.0;
      addScorePopup(player.x, player.y - 70, "🧲 MAGNET ACTIVE!", COLORS.GOLD);
    } else if (type === 'SHIELD') {
      shieldActive = true;
      addScorePopup(player.x, player.y - 70, "🛡️ SHIELD READY!", COLORS.CYAN);
    } else if (type === 'SLOWMO') {
      slowmoTime = 6.0;
      addScorePopup(player.x, player.y - 70, "⏱️ ZERO-G SLOW-MO!", COLORS.PURPLE);
    } else if (type === 'SUGAR_RUSH') {
      sugarRushCount = 6;
      addScorePopup(player.x, player.y - 70, "🍓 2X SUGAR RUSH!", COLORS.PINK);
    }
  }

  function startGame(startStage = 1, initialScore = 0) {
    score = initialScore;
    lives = MAX_LIVES;
    stage = startStage;
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    shakeTime = 0;
    comboStreak = 0;
    magnetTime = 0;
    shieldActive = false;
    slowmoTime = 0;
    sugarRushCount = 0;
    powerupSpawnTimer = 14;
    hazardWarnings = [];
    ceremonyCandles = [];
    ceremonyAllBlown = false;
    ceremonySmokeParticles = [];
    items = [];
    particles = [];
    trails = [];
    player.x = WIDTH / 2;
    player.invincible = 0;
    targetX = player.x;
    state = 'PLAYING';
    stopMic();
    stopHappyBirthdaySong();
    btnAction.textContent = 'PAUSE';
    syncUIState();
  }

  function resumeCheckpoint() {
    const cpStage = parseInt(localStorage.getItem('anti_grav_checkpoint') || '1');
    const cpScore = parseInt(localStorage.getItem('anti_grav_checkpoint_score') || '0');
    startGame(cpStage, cpScore);
  }

  function continueMilestone() {
    stopMic();
    stopHappyBirthdaySong();
    stage++;
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    items = [];
    hazardWarnings = [];
    comboStreak = 0;
    ceremonyCandles = [];
    ceremonyAllBlown = false;
    ceremonySmokeParticles = [];
    state = 'PLAYING';
    btnAction.textContent = 'PAUSE';
    syncUIState();
    sfxCatch();
    haptic(30);
  }

  function nextStage() {
    stopMic();
    stopHappyBirthdaySong();
    stage++;
    if (stage > TOTAL_STAGES) {
      score += 2000;
      if (score > hiScore) {
        hiScore = score;
        localStorage.setItem('anti_grav_hiscore', hiScore);
      }
      state = 'WIN';
      btnAction.textContent = 'AGAIN';
      playHappyBirthdaySong();
      haptic([40, 50, 40, 50, 100]);
      syncUIState();
    } else {
      itemsCaughtStage = 0;
      timeLeft = STAGE_DURATION;
      items = [];
      hazardWarnings = [];
      state = 'PLAYING';
      btnAction.textContent = 'PAUSE';
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

  // ─── PARALLAX DEEP SPACE BAKERY WONDERS ─────────────────────────────

  function drawDonutGalaxy(ctx, gx, gy, sz, angle) {
    ctx.save();
    ctx.translate(gx, gy);
    ctx.rotate(angle);

    // Nebula glow
    const gGrad = ctx.createRadialGradient(0, 0, sz * 0.2, 0, 0, sz * 1.6);
    gGrad.addColorStop(0, 'rgba(255, 77, 166, 0.28)');
    gGrad.addColorStop(0.65, 'rgba(160, 32, 240, 0.12)');
    gGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = gGrad;
    ctx.beginPath(); ctx.arc(0, 0, sz * 1.6, 0, Math.PI * 2); ctx.fill();

    // Golden dough ring
    ctx.fillStyle = '#c68b59';
    ctx.beginPath(); ctx.arc(0, 0, sz, 0, Math.PI * 2); ctx.fill();

    // Strawberry pink glaze
    ctx.fillStyle = '#ff6ebe';
    ctx.beginPath(); ctx.arc(0, 0, sz * 0.90, 0, Math.PI * 2); ctx.fill();

    // Glaze gloss highlight
    ctx.fillStyle = '#ffb3c6';
    ctx.beginPath();
    ctx.arc(-sz * 0.25, -sz * 0.25, sz * 0.45, -Math.PI * 0.8, -Math.PI * 0.2);
    ctx.lineWidth = 4;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
    ctx.stroke();

    // Center cosmic donut hole
    ctx.fillStyle = '#080417';
    ctx.beginPath(); ctx.arc(0, 0, sz * 0.42, 0, Math.PI * 2); ctx.fill();

    // Orbiting rainbow sprinkles
    const spCols = ['#00dcff', '#ffd700', '#ffffff', '#37be46', '#ff0055'];
    for (let i = 0; i < 14; i++) {
      const a = (i / 14) * Math.PI * 2 + 0.35;
      const r = sz * 0.68;
      ctx.fillStyle = spCols[i % spCols.length];
      ctx.fillRect(Math.cos(a) * r - 2.5, Math.sin(a) * r - 1.5, 5, 3);
    }
    ctx.restore();
  }

  function drawMacaronPlanet(ctx, px, py, r) {
    ctx.save();
    ctx.translate(px, py);

    // Planet sphere
    const pGrad = ctx.createRadialGradient(-r * 0.3, -r * 0.3, r * 0.1, 0, 0, r);
    pGrad.addColorStop(0, '#ba68c8');
    pGrad.addColorStop(0.7, '#7b1fa2');
    pGrad.addColorStop(1, '#38006b');
    ctx.fillStyle = pGrad;
    ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill();

    // Golden Macaron Planetary Ring
    ctx.save();
    ctx.rotate(0.38);
    ctx.scale(1.0, 0.32);
    ctx.strokeStyle = 'rgba(255, 215, 0, 0.8)';
    ctx.lineWidth = 6;
    ctx.beginPath(); ctx.arc(0, 0, r * 2.1, 0, Math.PI * 2); ctx.stroke();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(0, 0, r * 2.3, 0, Math.PI * 2); ctx.stroke();
    ctx.restore();

    ctx.restore();
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

  function drawGiftbox(ctx, x, y, rot, powerType) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.4, 1.4);

    // Glowing aura
    ctx.shadowColor = '#ffd700';
    ctx.shadowBlur = 16;

    // Box body
    ctx.fillStyle = '#ff0055';
    ctx.fillRect(-14, -10, 28, 24);

    // Gold ribbon
    ctx.fillStyle = '#ffd700';
    ctx.fillRect(-4, -10, 8, 24);
    ctx.fillRect(-14, 0, 28, 6);

    // Lid
    ctx.fillStyle = '#d60045';
    ctx.fillRect(-16, -14, 32, 6);
    ctx.fillStyle = '#ffd700';
    ctx.fillRect(-4, -14, 8, 6);

    // Bow on top
    ctx.strokeStyle = '#ffd700';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(-5, -17, 5, 0, Math.PI * 2);
    ctx.arc(5, -17, 5, 0, Math.PI * 2);
    ctx.stroke();

    // Power icon badge
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 9px sans-serif';
    ctx.textAlign = 'center';
    const icon = (powerType === 'MAGNET') ? '🧲' : (powerType === 'SHIELD' ? '🛡️' : (powerType === 'SLOWMO' ? '⏱️' : '🍓'));
    ctx.fillText(icon, 0, 8);

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

    // Character Ghost Dash Trails
    ghostTrails = ghostTrails.filter(gt => gt.alpha > 0);
    ghostTrails.forEach(gt => {
      gt.alpha -= dt * 2.5;
    });

    // Cosmic Candy Comets
    cometTimer -= dt;
    if (cometTimer <= 0) {
      cometTimer = 7.0 + Math.random() * 8.0;
      candyComets.push({
        x: -40,
        y: 80 + Math.random() * (HEIGHT * 0.4),
        vx: 320 + Math.random() * 120,
        vy: 160 + Math.random() * 80,
        color: ['#ff4da6', '#ffd700', '#00dcff', '#a03ce6'][Math.floor(Math.random() * 4)],
        life: 3.5
      });
    }
    candyComets = candyComets.filter(cc => cc.life > 0);
    candyComets.forEach(cc => {
      cc.x += cc.vx * dt;
      cc.y += cc.vy * dt;
      cc.life -= dt;
      if (Math.random() < 0.6) {
        trails.push({
          x: cc.x + (Math.random() - 0.5) * 6,
          y: cc.y + (Math.random() - 0.5) * 6,
          vy: -10,
          life: 0.7,
          color: cc.color
        });
      }
    });

    // Particles
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
    });

    // Candle Ceremony Smoke Particles
    ceremonySmokeParticles = ceremonySmokeParticles.filter(p => p.life > 0);
    ceremonySmokeParticles.forEach(p => {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.radius += dt * 7;
      p.life -= dt;
      p.alpha = Math.max(0, p.life / p.maxLife);
    });

    // Real Microphone Breath Detection in Ceremony
    if (state === 'CANDLE_CEREMONY' && micEnabled && micAnalyser && micDataArray && !ceremonyAllBlown) {
      micAnalyser.getByteFrequencyData(micDataArray);
      let sum = 0;
      for (let i = 4; i < micDataArray.length; i++) {
        sum += micDataArray[i];
      }
      const avg = sum / (micDataArray.length - 4);
      micBlowLevel = Math.min(1.0, avg / 75.0);

      if (avg > 36) {
        micBlowFrames++;
        // Generate visible breath wind stream
        if (Math.random() < 0.6) {
          ceremonySmokeParticles.push({
            x: WIDTH / 2 + (Math.random() - 0.5) * 180,
            y: HEIGHT / 2 + 100,
            vx: (Math.random() - 0.5) * 35,
            vy: -75 - Math.random() * 55,
            radius: 3.5 + Math.random() * 4,
            life: 0.8,
            maxLife: 0.8,
            alpha: 0.65
          });
        }
        if (micBlowFrames >= 3) {
          blowCandles();
          micBlowFrames = 0;
        }
      } else {
        micBlowFrames = Math.max(0, micBlowFrames - 1);
      }
    }

    if (state === 'PLAYING') {
      btnAction.textContent = 'PAUSE';

      // Power-up timers
      if (slowmoTime > 0) slowmoTime -= dt;

      // Player Movement (responsive drag + keys + buttons)
      let moveDir = 0;
      if (keys['ArrowLeft'] || keys['KeyA']) moveDir -= 1;
      if (keys['ArrowRight'] || keys['KeyD']) moveDir += 1;

      // Compute player velocity & bank tilt
      const curX = player.x;
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
      player.vx = (player.x - player.prevX) / Math.max(0.001, dt);
      player.prevX = player.x;

      // Bank tilt towards movement
      const targetTilt = Math.max(-0.11, Math.min(0.11, player.vx * 0.00022));
      player.tilt += (targetTilt - player.tilt) * Math.min(1.0, 14 * dt);

      // Ghost dash speed silhouette trail
      if (Math.abs(player.vx) > 180 && Math.random() < 0.42) {
        ghostTrails.push({
          x: player.x,
          y: player.y,
          tilt: player.tilt,
          alpha: 0.5,
          color: (comboStreak >= 10 ? '#ff00ff' : (comboStreak >= 5 ? '#ffd700' : '#00dcff'))
        });
      }

      // Cake Squash & Stretch spring physics
      player.traySquashVel += (1.0 - player.traySquash) * 48 * dt;
      player.traySquashVel *= 0.80;
      player.traySquash += player.traySquashVel * dt;

      // Micro-expressions timers
      player.happyTime = Math.max(0, player.happyTime - dt);
      player.worryTime = Math.max(0, player.worryTime - dt);

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

      // Spawner & Hazard Warnings
      const speed = 190 + Math.min(360, (stage - 1) * 12.5);
      const interval = Math.max(0.40, 1.15 - (stage - 1) * 0.025);
      spawnTimer -= dt;
      if (spawnTimer <= 0) {
        spawnTimer = interval;
        const isBad = Math.random() < Math.min(0.45, 0.28 + (stage - 1) * 0.006);
        const minX = Math.min(90, WIDTH * 0.12);
        const maxX = WIDTH - minX;
        const itemX = minX + Math.random() * (maxX - minX);

        if (isBad) {
          const kind = BAD_KINDS[Math.floor(Math.random() * BAD_KINDS.length)];
          hazardWarnings.push({
            x: itemX,
            timer: 0.45,
            kind: kind,
            vy: speed,
            vrot: (Math.random() - 0.5) * 4.5
          });
        } else {
          const kind = GOOD_KINDS[Math.floor(Math.random() * GOOD_KINDS.length)];
          items.push({
            x: itemX,
            y: -40,
            vy: speed,
            isBad: false,
            isPowerup: false,
            kind: kind,
            pts: 50,
            rot: 0,
            vrot: (Math.random() - 0.5) * 4.5,
            color: kind === 'CAKE' ? COLORS.PINK : COLORS.GOLD
          });
        }
      }

      // Process Hazard Warnings (release dropping obstacles)
      for (let w = hazardWarnings.length - 1; w >= 0; w--) {
        hazardWarnings[w].timer -= dt;
        if (hazardWarnings[w].timer <= 0) {
          const hw = hazardWarnings[w];
          items.push({
            x: hw.x,
            y: -35,
            vy: hw.vy,
            isBad: true,
            isPowerup: false,
            kind: hw.kind,
            pts: 0,
            rot: 0,
            vrot: hw.vrot,
            color: COLORS.RED
          });
          hazardWarnings.splice(w, 1);
        }
      }

      // Occasional Power-Up Giftbox Spawner (~every 18s)
      powerupSpawnTimer -= dt;
      if (powerupSpawnTimer <= 0) {
        powerupSpawnTimer = 16 + Math.random() * 8;
        const minX = Math.min(90, WIDTH * 0.12);
        const maxX = WIDTH - minX;
        items.push({
          x: minX + Math.random() * (maxX - minX),
          y: -40,
          vy: speed * 0.85,
          isBad: false,
          isPowerup: true,
          powerType: ['MAGNET', 'SHIELD', 'SLOWMO', 'SUGAR_RUSH'][Math.floor(Math.random() * 4)],
          rot: 0,
          vrot: (Math.random() - 0.5) * 3,
          color: COLORS.GOLD
        });
      }

      // Cake height dynamically grows with items caught (out of 20 per stage)
      const cakeLayersH = (itemsCaughtStage >= 14 ? 68 : (itemsCaughtStage >= 7 ? 38 : 20)) * 1.25;
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

      // Golden Whisk Magnet Effect: Pull nearby good items towards tray
      if (magnetTime > 0) {
        magnetTime -= dt;
        items.forEach(it => {
          if (!it.isBad) {
            const d = Math.abs(player.x - it.x);
            if (d < 300 && it.y < trayRect.y + 40) {
              it.x += (player.x - it.x) * Math.min(1.0, 5.0 * dt);
            }
          }
        });
      }

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
        const curVy = (item.isBad && slowmoTime > 0) ? item.vy * 0.52 : item.vy;
        item.y += curVy * dt;
        item.rot += item.vrot * dt;

        // Leave stardust trail
        if (Math.random() < 0.35) {
          trails.push({
            x: item.x + (Math.random() - 0.5) * 8,
            y: item.y - 10,
            vy: -15,
            life: 0.8,
            color: item.isBad ? 'rgba(255, 50, 70, 0.6)' : (item.isPowerup ? 'rgba(255, 215, 0, 0.8)' : 'rgba(0, 255, 136, 0.6)')
          });
        }

        // Catch check
        if (!item.isBad) {
          if (item.x >= trayRect.x && item.x <= trayRect.x + trayRect.w &&
              item.y >= trayRect.y && item.y <= trayRect.y + trayRect.h + 24) {

            // Cake Squash & Stretch Jiggle + Character Happy Expression
            player.traySquash = 0.72;
            player.happyTime = 0.65;

            // Frosting Splatters & Rainbow Sprinkles on Catch
            const splashCols = ['#ff4da6', '#ffffff', '#ffd700', '#00dcff', '#ff8500', '#70e000'];
            for (let sp = 0; sp < 10; sp++) {
              particles.push({
                x: item.x + (Math.random() - 0.5) * 32,
                y: player.y - 95,
                vx: (Math.random() - 0.5) * 160,
                vy: -75 - Math.random() * 95,
                size: 2.5 + Math.random() * 3,
                color: splashCols[sp % splashCols.length],
                life: 0.55,
                maxLife: 0.55
              });
            }

            if (item.isPowerup) {
              score += 100;
              itemsCaughtStage = Math.min(ITEMS_PER_STAGE, itemsCaughtStage + 1);
              activatePowerup(item.powerType);
              addCollectBurst(item.x, item.y, COLORS.GOLD);
              sfxPowerup();
              haptic(25);
              items.splice(i, 1);
            } else {
              let ptsAwarded = 50;
              let popupText = "+50";
              if (sugarRushCount > 0) {
                sugarRushCount--;
                ptsAwarded = 100;
                popupText = "+100 (2X!)";
              }
              score += ptsAwarded;
              itemsCaughtStage++;
              comboStreak++;

              if (comboStreak === 5) {
                score += 75;
                addScorePopup(player.x, player.y - 75, "5x COMBO! +75", COLORS.GOLD);
                sfxCombo();
              } else if (comboStreak >= 10 && comboStreak % 5 === 0) {
                score += 150;
                addScorePopup(player.x, player.y - 75, comboStreak + "x BAKING FEVER! +150", '#00f0ff');
                addCollectBurst(player.x, player.y - 60, '#00f0ff');
                sfxCombo();
              }

              addCollectBurst(item.x, item.y, '#00ff88');
              addScorePopup(item.x, item.y - 20, popupText, sugarRushCount > 0 ? '#ff6ebe' : '#00ff88');
              sfxCatch();
              haptic(15);
              items.splice(i, 1);
            }

            if (itemsCaughtStage >= ITEMS_PER_STAGE) {
              if (stage % 5 === 0) {
                score += 500;
                state = 'CANDLE_CEREMONY';
                initCandleCeremony();
                sfxWin();
                syncUIState();
              } else {
                score += 500;
                state = 'STAGE_CLEAR';
                stageClearTime = 1.8;
                addCollectBurst(WIDTH / 2, HEIGHT / 2, COLORS.GOLD);
                sfxWin();
                haptic([30, 30, 60]);
              }
            }
            continue;
          }
        } else {
          // Obstacle collision
          if (player.invincible <= 0) {
            if (item.x >= bodyRect.x && item.x <= bodyRect.x + bodyRect.w &&
                item.y >= bodyRect.y && item.y <= bodyRect.y + bodyRect.h) {

              if (shieldActive) {
                shieldActive = false;
                player.invincible = 1.2;
                shakeTime = 0.2;
                addScorePopup(player.x, player.y - 50, "SHIELD BLOCKED!", COLORS.CYAN);
                addCollectBurst(item.x, item.y, COLORS.CYAN);
                sfxCatch();
                haptic([30, 40]);
                items.splice(i, 1);
                continue;
              }

              comboStreak = 0;
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

        // Check hazard proximity to Aisha's head (triggers worried sweatdrop!)
        if (item.isBad) {
          if (Math.abs(item.x - player.x) < 70 && Math.abs(item.y - (player.y - 75)) < 70) {
            player.worryTime = 0.45;
          }
          // Anvil Floor Slam with Sparks & Screen Shudder
          if (item.kind === 'ANVIL' && !item.slammedFloor && item.y >= HEIGHT - 54) {
            item.slammedFloor = true;
            shakeTime = 0.16;
            for (let sp = 0; sp < 8; sp++) {
              particles.push({
                x: item.x + (Math.random() - 0.5) * 18,
                y: HEIGHT - 50,
                vx: (Math.random() - 0.5) * 170,
                vy: -40 - Math.random() * 85,
                size: 2.5 + Math.random() * 2.5,
                color: '#ffd700',
                life: 0.35,
                maxLife: 0.35
              });
            }
            playTone(160, 'sawtooth', 0.1, 0.22);
          }
        }

        // Clean off-screen
        if (item.y > HEIGHT + 40) {
          if (!item.isBad && !item.isPowerup) {
            comboStreak = 0;
          }
          items.splice(i, 1);
        }
      }
    } else if (state === 'STAGE_CLEAR') {
      stageClearTime -= dt;
      if (stageClearTime <= 0) nextStage();
    } else if (state === 'WIN' || state === 'MILESTONE' || state === 'CANDLE_CEREMONY') {
      if (ceremonyAllBlown || state === 'WIN' || state === 'MILESTONE') {
        if (Math.random() < 0.08) {
          addFireworks(100 + Math.random() * (WIDTH - 200), 100 + Math.random() * (HEIGHT * 0.5),
                       bColors[Math.floor(Math.random() * bColors.length)]);
        }
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

    // Dynamic Cosmic Themes across the 30 stages
    let bgGrad;
    if (stage <= 10) {
      // Theme 1: Deep Space Party (Stages 1-10)
      bgGrad = ctx.createRadialGradient(WIDTH / 2, HEIGHT / 2, 50, WIDTH / 2, HEIGHT / 2, HEIGHT * 0.8);
      bgGrad.addColorStop(0, '#1a1040');
      bgGrad.addColorStop(0.65, '#0b0621');
      bgGrad.addColorStop(1, '#050210');
    } else if (stage <= 20) {
      // Theme 2: Sunset Galaxy (Stages 11-20)
      bgGrad = ctx.createRadialGradient(WIDTH / 2, HEIGHT / 2, 50, WIDTH / 2, HEIGHT / 2, HEIGHT * 0.8);
      bgGrad.addColorStop(0, '#361138');
      bgGrad.addColorStop(0.65, '#1b0626');
      bgGrad.addColorStop(1, '#090112');
    } else {
      // Theme 3: Cosmic Cyber-Disco (Stages 21-30)
      bgGrad = ctx.createRadialGradient(WIDTH / 2, HEIGHT / 2, 50, WIDTH / 2, HEIGHT / 2, HEIGHT * 0.8);
      bgGrad.addColorStop(0, '#1f0942');
      bgGrad.addColorStop(0.65, '#0c0228');
      bgGrad.addColorStop(1, '#030010');
    }
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Glowing Nebula clouds (pulsing in sync with chiptune beat during combos!)
    ctx.save();
    const comboPulse = (comboStreak >= 5) ? (Math.sin(globalTime * 9) * 0.10) : 0;
    ctx.globalAlpha = 0.22 + comboPulse;
    const neb1Col = stage <= 10 ? '#ff00aa' : (stage <= 20 ? '#ff7700' : '#bd00ff');
    const neb2Col = stage <= 10 ? '#00dcff' : (stage <= 20 ? '#ff0077' : '#00f0ff');
    const neb1 = ctx.createRadialGradient(WIDTH * 0.25, HEIGHT * 0.35, 10, WIDTH * 0.25, HEIGHT * 0.35, 260);
    neb1.addColorStop(0, neb1Col); neb1.addColorStop(1, 'transparent');
    ctx.fillStyle = neb1; ctx.fillRect(0, 0, WIDTH, HEIGHT);

    const neb2 = ctx.createRadialGradient(WIDTH * 0.75, HEIGHT * 0.65, 10, WIDTH * 0.75, HEIGHT * 0.65, 280);
    neb2.addColorStop(0, neb2Col); neb2.addColorStop(1, 'transparent');
    ctx.fillStyle = neb2; ctx.fillRect(0, 0, WIDTH, HEIGHT);
    ctx.restore();

    // Parallax Deep-Space Wonders: Donut Galaxy & Macaron Saturn Planet
    drawDonutGalaxy(ctx, WIDTH * 0.22, HEIGHT * 0.24, 38, globalTime * 0.15);
    drawMacaronPlanet(ctx, WIDTH * 0.78, HEIGHT * 0.28, 28);

    // Cosmic Candy Comets
    candyComets.forEach(cc => {
      ctx.save();
      ctx.fillStyle = cc.color;
      ctx.shadowColor = cc.color;
      ctx.shadowBlur = 14;
      ctx.beginPath();
      ctx.arc(cc.x, cc.y, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(cc.x - 2, cc.y - 2, 2.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });

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

    // Hazard Drop Warning Markers (exclamation marks at column top)
    hazardWarnings.forEach(hw => {
      ctx.save();
      const flash = Math.sin(globalTime * 30) > 0;
      ctx.translate(hw.x, 62);
      ctx.fillStyle = flash ? '#ff2040' : '#880015';
      ctx.shadowColor = '#ff2040';
      ctx.shadowBlur = flash ? 16 : 4;
      ctx.beginPath();
      ctx.moveTo(0, -14); ctx.lineTo(14, 0); ctx.lineTo(0, 14); ctx.lineTo(-14, 0);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('!', 0, 4);
      ctx.strokeStyle = flash ? 'rgba(255, 30, 60, 0.45)' : 'rgba(255, 30, 60, 0.12)';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(0, 14); ctx.lineTo(0, 95); ctx.stroke();
      ctx.restore();
    });

    // Hazard Floor Drop-Shadows (Target Footprints for mobile dodging accuracy)
    items.forEach(item => {
      if (item.isBad) {
        const floorY = HEIGHT - 50;
        const dist = floorY - item.y;
        if (dist > 0 && dist < 680) {
          const t = 1.0 - (dist / 680);
          const rad = 14 + t * 24;
          const alpha = 0.20 + t * 0.65;
          ctx.save();
          ctx.translate(item.x, floorY);
          ctx.scale(1.0, 0.35);

          // Translucent warning landing disc
          ctx.fillStyle = `rgba(255, 30, 60, ${alpha * 0.35})`;
          ctx.beginPath(); ctx.arc(0, 0, rad, 0, Math.PI * 2); ctx.fill();

          // Outer dashed danger ring
          ctx.strokeStyle = `rgba(255, 40, 70, ${alpha})`;
          ctx.lineWidth = 2.5;
          ctx.setLineDash([4, 4]);
          ctx.beginPath(); ctx.arc(0, 0, rad, 0, Math.PI * 2); ctx.stroke();
          ctx.setLineDash([]);

          // Imminent landing alert '!'
          if (dist < 220) {
            ctx.scale(1.0, 1 / 0.35);
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px sans-serif';
            ctx.textAlign = 'center';
            ctx.shadowColor = '#ff1144';
            ctx.shadowBlur = 8;
            ctx.fillText('!', 0, -6);
          }
          ctx.restore();
        }
      }
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
      } else if (item.isPowerup) {
        // Shimmering Golden Power-Up Aura
        grad.addColorStop(0, 'rgba(255, 215, 0, 0)');
        grad.addColorStop(0.65, 'rgba(255, 215, 0, 0.35)');
        grad.addColorStop(1, 'rgba(255, 215, 0, 0.7)');
        ctx.fillStyle = grad;
        ctx.fillRect(item.x - 26, item.y - trailH, 52, trailH + 20);
        ctx.shadowColor = '#ffd700';
        ctx.shadowBlur = 20;
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
      if (item.isPowerup) drawGiftbox(ctx, item.x, item.y, item.rot, item.powerType);
      else if (item.kind === 'CAKE') drawCake(ctx, item.x, item.y, item.rot);
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

    // Character Ghost Dash Afterimage Trails
    if (state === 'PLAYING') {
      ghostTrails.forEach(gt => {
        ctx.save();
        ctx.globalAlpha = Math.max(0, gt.alpha * 0.55);
        ctx.translate(gt.x, gt.y);
        ctx.scale(1.25, 1.25);
        ctx.rotate(gt.tilt || 0);
        ctx.fillStyle = gt.color;
        ctx.shadowColor = gt.color;
        ctx.shadowBlur = 14;
        ctx.fillRect(-16, -14, 32, 24);
        ctx.fillRect(-16, 14, 32, 25);
        ctx.beginPath(); ctx.ellipse(0, -36, 18, 22, 0, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      });
    }

    // Playable Character (Aisha) — Scaled 1.25x with dynamic bank tilt & cake jiggle
    if (state === 'PLAYING' || state === 'STAGE_CLEAR' || state === 'PAUSED') {
      const flicker = player.invincible > 0 && Math.floor(player.invincible * 14) % 2 === 0;
      if (!flicker) {
        ctx.save();
        const bob = Math.sin(player.walkTime) * 3;
        const px = player.x;
        const py = player.y + bob;

        ctx.translate(px, py);
        ctx.scale(1.25, 1.25);
        ctx.rotate(player.tilt);

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

        // Micro-Expressions: Cheerful Sparkle & Blush on Catch
        if (player.happyTime > 0) {
          ctx.fillStyle = '#ffd700';
          ctx.shadowColor = '#ffd700';
          ctx.shadowBlur = 8;
          ctx.fillRect(10, headY - 4, 5, 5);
          ctx.fillRect(8, headY - 2, 9, 2);
          ctx.fillRect(11, headY - 5, 2, 8);

          // Pink blush cheeks
          ctx.fillStyle = 'rgba(255, 77, 166, 0.65)';
          ctx.beginPath();
          ctx.arc(-11, headY + 5, 4, 0, Math.PI * 2);
          ctx.arc(11, headY + 5, 4, 0, Math.PI * 2);
          ctx.fill();
        }

        // Micro-Expressions: Animated Blue Sweatdrop on Hazard Near-Miss
        if (player.worryTime > 0) {
          const swHop = Math.sin(globalTime * 28) * 3;
          ctx.fillStyle = '#00dcff';
          ctx.shadowColor = '#00dcff';
          ctx.shadowBlur = 8;
          ctx.beginPath();
          ctx.moveTo(headRx + 5, headY - 8 + swHop);
          ctx.quadraticCurveTo(headRx + 12, headY - 2 + swHop, headRx + 6, headY + 5 + swHop);
          ctx.quadraticCurveTo(headRx + 1, headY - 2 + swHop, headRx + 5, headY - 8 + swHop);
          ctx.fill();
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(headRx + 4, headY - 3 + swHop, 2, 2);
        }

        // 6. Unlockable Costumes (Party Hat / Royal Crown / Chef Toque / Diamond Tiara)
        if (stage >= 30) {
          // Tier 4 (Stage 30): Sparkling Diamond Birthday Tiara + Rainbow Stardust
          const tiaraBaseY = headY - headRy + 3;
          const tiaraW = 34;
          ctx.strokeStyle = '#e0f7fa';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(-tiaraW / 2, tiaraBaseY);
          ctx.quadraticCurveTo(0, tiaraBaseY - 6, tiaraW / 2, tiaraBaseY);
          ctx.stroke();

          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(-tiaraW / 2, tiaraBaseY);
          ctx.lineTo(-tiaraW / 3, tiaraBaseY - 12);
          ctx.lineTo(-tiaraW / 6, tiaraBaseY - 6);
          ctx.lineTo(0, tiaraBaseY - 24);
          ctx.lineTo(tiaraW / 6, tiaraBaseY - 6);
          ctx.lineTo(tiaraW / 3, tiaraBaseY - 12);
          ctx.lineTo(tiaraW / 2, tiaraBaseY);
          ctx.stroke();

          ctx.fillStyle = '#ff0077';
          ctx.beginPath();
          ctx.arc(-2, tiaraBaseY - 12, 2.5, 0, Math.PI * 2);
          ctx.arc(2, tiaraBaseY - 12, 2.5, 0, Math.PI * 2);
          ctx.fill();
          ctx.beginPath();
          ctx.moveTo(-4.5, tiaraBaseY - 11); ctx.lineTo(0, tiaraBaseY - 6); ctx.lineTo(4.5, tiaraBaseY - 11);
          ctx.fill();

          const dGems = ['#00ffff', '#ffffff', '#ffd700', '#ff66cc'];
          [[-tiaraW / 3, tiaraBaseY - 12], [0, tiaraBaseY - 24], [tiaraW / 3, tiaraBaseY - 12]].forEach(([dx, dy], idx) => {
            ctx.fillStyle = dGems[(idx + Math.floor(globalTime * 6)) % dGems.length];
            ctx.shadowColor = '#00ffff';
            ctx.shadowBlur = 8;
            ctx.beginPath();
            ctx.arc(dx, dy, 3, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
          });

          if (Math.random() < 0.35) {
            trails.push({
              x: px + (Math.random() - 0.5) * 36,
              y: py - 40 + (Math.random() - 0.5) * 20,
              vy: -18,
              life: 0.55,
              color: ['#00ffff', '#ff66cc', '#ffd700', '#37be46'][Math.floor(Math.random() * 4)]
            });
          }
        } else if (stage >= 20) {
          // Tier 3 (Stages 20-29): Master Chef Toque with Pink Satin Ribbon & Gold Buckle
          const toqueBaseY = headY - headRy + 3;
          const toqueW = 32;
          ctx.fillStyle = '#ff4da6';
          ctx.fillRect(-toqueW / 2 + 2, toqueBaseY - 6, toqueW - 4, 7);
          ctx.fillStyle = '#ffd700';
          ctx.fillRect(-3, toqueBaseY - 5, 6, 5);

          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.moveTo(-toqueW / 2 + 2, toqueBaseY - 6);
          ctx.bezierCurveTo(-toqueW / 2 - 6, toqueBaseY - 22, -toqueW / 4, toqueBaseY - 28, -toqueW / 6, toqueBaseY - 26);
          ctx.bezierCurveTo(-toqueW / 8, toqueBaseY - 32, toqueW / 8, toqueBaseY - 32, toqueW / 6, toqueBaseY - 26);
          ctx.bezierCurveTo(toqueW / 4, toqueBaseY - 28, toqueW / 2 + 6, toqueBaseY - 22, toqueW / 2 - 2, toqueBaseY - 6);
          ctx.closePath();
          ctx.fill();

          ctx.strokeStyle = '#e2e8f0';
          ctx.lineWidth = 1.5;
          [-6, 0, 6].forEach(fx => {
            ctx.beginPath();
            ctx.moveTo(fx, toqueBaseY - 7);
            ctx.lineTo(fx * 1.2, toqueBaseY - 24);
            ctx.stroke();
          });
        } else if (stage >= 10) {
          // Tier 2 (Stages 10-19): Golden Royal Baker Crown with Ruby & Sapphire Jewels
          const crownBaseY = headY - headRy + 3;
          const crownH = 20;
          const crownW = 30;
          ctx.fillStyle = '#d48800';
          ctx.fillRect(-crownW / 2, crownBaseY - 5, crownW, 6);
          ctx.fillStyle = '#ffd700';
          ctx.fillRect(-crownW / 2, crownBaseY - 4, crownW, 4);

          ctx.beginPath();
          ctx.moveTo(-crownW / 2, crownBaseY - 5);
          ctx.lineTo(-crownW / 2, crownBaseY - crownH);
          ctx.lineTo(-crownW / 4, crownBaseY - crownH * 0.55);
          ctx.lineTo(-crownW / 8, crownBaseY - crownH * 1.05);
          ctx.lineTo(0, crownBaseY - crownH * 0.65);
          ctx.lineTo(crownW / 8, crownBaseY - crownH * 1.05);
          ctx.lineTo(crownW / 4, crownBaseY - crownH * 0.55);
          ctx.lineTo(crownW / 2, crownBaseY - crownH);
          ctx.lineTo(crownW / 2, crownBaseY - 5);
          ctx.closePath();
          ctx.fill();

          ctx.strokeStyle = '#fff5a0';
          ctx.lineWidth = 1.2;
          ctx.stroke();

          ctx.fillStyle = '#ff1144';
          ctx.fillRect(-2, crownBaseY - 5, 4, 4);
          ctx.fillStyle = '#00dcff';
          ctx.fillRect(-crownW / 3, crownBaseY - 4, 3, 3);
          ctx.fillRect(crownW / 3 - 3, crownBaseY - 4, 3, 3);

          ctx.fillStyle = '#ffffff';
          [[-crownW / 2, crownBaseY - crownH], [-crownW / 8, crownBaseY - crownH * 1.05], [crownW / 8, crownBaseY - crownH * 1.05], [crownW / 2, crownBaseY - crownH]].forEach(([pxo, pyo]) => {
            ctx.beginPath(); ctx.arc(pxo, pyo, 2, 0, Math.PI * 2); ctx.fill();
          });
          if (Math.sin(globalTime * 8) > 0.6) {
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, crownBaseY - crownH * 0.85, 3, 3);
          }
        } else {
          // Tier 1 (Stages 1-9): Classic Pink Party Hat with Polka Dots & Gold Pompom
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
          ctx.fillStyle = '#ffd700';
          ctx.beginPath();
          ctx.arc(0, hatTipY - 2, 3.5, 0, Math.PI * 2);
          ctx.fill();
        }

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

        // 8. Multi-Layered Cake with Squash & Stretch Jiggle Physics
        ctx.save();
        ctx.translate(0, trayY);
        ctx.scale(1.0 / Math.sqrt(Math.max(0.6, player.traySquash)), player.traySquash);
        ctx.translate(0, -trayY);

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

        // Tier 2 Layer (grows if itemsCaughtStage >= 7)
        if (itemsCaughtStage >= 7) {
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

        // Tier 3 Layer (grows if itemsCaughtStage >= 14)
        if (itemsCaughtStage >= 14) {
          const t3W = 42, t3H = 14;
          const t3Y = t1Y - 16 - t3H;
          ctx.fillStyle = '#c040ff';
          ctx.fillRect(-t3W / 2, t3Y, t3W, t3H);
          ctx.fillStyle = '#00dcff';
          ctx.fillRect(-t3W / 2, t3Y + 3, t3W, 2);
        }

        // Birthday Candles (flickering on top of highest layer)
        const topY = itemsCaughtStage >= 14 ? (t1Y - 30) : (itemsCaughtStage >= 7 ? (t1Y - 16) : t1Y);
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
        ctx.restore(); // End Cake Squash & Stretch

        // Frosting Shield Bubble around Aisha
        if (shieldActive) {
          ctx.save();
          const shieldPulse = Math.sin(globalTime * 6) * 3;
          ctx.shadowColor = '#00f0ff';
          ctx.shadowBlur = 18;
          ctx.strokeStyle = 'rgba(0, 240, 255, 0.85)';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(0, -30, 70 + shieldPulse, 0, Math.PI * 2);
          ctx.stroke();

          ctx.fillStyle = 'rgba(0, 220, 255, 0.12)';
          ctx.fill();

          for (let si = 0; si < 3; si++) {
            const sAngle = globalTime * 4 + si * (Math.PI * 2 / 3);
            const sx = Math.cos(sAngle) * (70 + shieldPulse);
            const sy = -30 + Math.sin(sAngle) * (70 + shieldPulse);
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(sx - 3, sy - 3, 6, 6);
          }
          ctx.restore();
        }

        ctx.restore();
      }
    }

    // Particles & Floating Text Popups
    particles.forEach(p => {
      ctx.save();
      const alpha = Math.max(0, p.life / p.maxLife);
      if (p.isText) {
        const progress = 1.0 - (p.life / p.maxLife);
        const popScale = 1.0 + Math.sin(progress * Math.PI) * 0.42;
        ctx.translate(p.x, p.y);
        ctx.scale(popScale, popScale);
        ctx.fillStyle = p.color;
        ctx.font = '13px "Press Start 2P", monospace';
        ctx.textAlign = 'center';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 4;
        ctx.strokeText(p.text, 0, 0);
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 10;
        ctx.fillText(p.text, 0, 0);
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
    const mins = Math.floor(secs / 60);
    const remSecs = secs % 60;
    const tStr = mins + ":" + String(remSecs).padStart(2, "0");
    const tCol = (timeLeft < 10 && Math.floor(globalTime * 4) % 2 === 0) ? '#ff2a55' : '#00dcff';
    ctx.fillStyle = tCol;
    ctx.shadowColor = tCol;
    ctx.shadowBlur = 8;
    ctx.font = '16px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(tStr, WIDTH / 2, 35);
    ctx.restore();

    // Mini Cake Level Progress Bar (0 to 20 ingredients)
    const progW = 120;
    const progH = 6;
    const progX = WIDTH / 2 - progW / 2;
    const progY = 48;
    ctx.fillStyle = 'rgba(255, 255, 255, 0.22)';
    ctx.fillRect(progX, progY, progW, progH);
    const progRatio = Math.min(1.0, itemsCaughtStage / ITEMS_PER_STAGE);
    ctx.fillStyle = '#00ff88';
    ctx.shadowColor = '#00ff88';
    ctx.shadowBlur = 6;
    ctx.fillRect(progX, progY, progW * progRatio, progH);
    ctx.shadowBlur = 0;

    ctx.fillStyle = '#00dcff';
    ctx.font = '8px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText("🍰 " + itemsCaughtStage + "/" + ITEMS_PER_STAGE, WIDTH / 2, progY + 16);

    // Arcade Combo Fever Mode Badges & Screen Vignette
    if (state === 'PLAYING') {
      if (comboStreak >= 10) {
        // Golden/Rainbow Screen Border Vignette Glow
        ctx.save();
        const feverVignette = ctx.createRadialGradient(WIDTH / 2, HEIGHT / 2, HEIGHT * 0.42, WIDTH / 2, HEIGHT / 2, HEIGHT * 0.78);
        const fA = 0.22 + Math.sin(globalTime * 12) * 0.14;
        feverVignette.addColorStop(0, 'rgba(255, 215, 0, 0)');
        feverVignette.addColorStop(1, `rgba(255, 215, 0, ${fA})`);
        ctx.fillStyle = feverVignette;
        ctx.fillRect(0, 0, WIDTH, HEIGHT);
        ctx.restore();

        // Pulsing Rainbow Fever Banner
        ctx.save();
        const fScale = 1.0 + Math.sin(globalTime * 10) * 0.08;
        ctx.translate(WIDTH / 2, 108);
        ctx.scale(fScale, fScale);
        ctx.fillStyle = ['#ffd700', '#00f0ff', '#ff4da6', '#70e000'][Math.floor(globalTime * 8) % 4];
        ctx.shadowColor = '#00f0ff';
        ctx.shadowBlur = 14;
        ctx.font = 'bold 12px "Press Start 2P", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(`⚡ ${comboStreak}x BAKING FEVER! ⚡`, 0, 0);
        ctx.restore();
      } else if (comboStreak >= 5) {
        // 5x Sugar Rush Banner
        ctx.save();
        const rScale = 1.0 + Math.sin(globalTime * 8) * 0.06;
        ctx.translate(WIDTH / 2, 108);
        ctx.scale(rScale, rScale);
        ctx.fillStyle = '#ffd700';
        ctx.shadowColor = '#ffd700';
        ctx.shadowBlur = 10;
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(`★ ${comboStreak}x SUGAR RUSH! ★`, 0, 0);
        ctx.restore();
      }
    }

    // Active Power-up Badges in HUD
    let puY = 78;
    if (shieldActive) {
      ctx.fillStyle = '#00f0ff';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("🛡️ SHIELD READY", WIDTH / 2, puY);
      puY += 15;
    }
    if (magnetTime > 0) {
      ctx.fillStyle = '#ffd700';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`🧲 MAGNET (${Math.ceil(magnetTime)}s)`, WIDTH / 2, puY);
      puY += 15;
    }
    if (slowmoTime > 0) {
      ctx.fillStyle = '#d060ff';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`⏱️ SLOW-MO (${Math.ceil(slowmoTime)}s)`, WIDTH / 2, puY);
      puY += 15;
    }
    if (sugarRushCount > 0) {
      ctx.fillStyle = '#ff4da6';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`🍓 2X RUSH (${sugarRushCount})`, WIDTH / 2, puY);
      puY += 15;
    }

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

    const costumeTitle = stage >= 30 ? "💎 TIARA" : (stage >= 20 ? "🧑‍🍳 CHEF" : (stage >= 10 ? "👑 CROWN" : "🎀 PARTY"));
    ctx.fillStyle = stage >= 30 ? '#00f0ff' : (stage >= 20 ? '#ffffff' : (stage >= 10 ? '#ffd700' : '#ff6ebe'));
    ctx.font = '8px "Press Start 2P", monospace';
    ctx.fillText(costumeTitle, WIDTH - pw - 18, HEIGHT - 36);
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

      // Checkpoint resume option or new game prompt
      if (checkpointStage > 1) {
        ctx.fillStyle = COLORS.CYAN;
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.fillText(`★ CHECKPOINT: STAGE ${checkpointStage} (${checkpointScore.toLocaleString()} PTS) ★`, WIDTH / 2, boxY + 396);

        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '12px "Press Start 2P", monospace';
        ctx.fillText(`★ TAP TO RESUME STAGE ${checkpointStage} ★`, WIDTH / 2, boxY + 434);

        ctx.fillStyle = '#859bb8';
        ctx.font = '9px "Press Start 2P", monospace';
        ctx.fillText(`START LVL 1 BELOW   |   BEST: ${hiScore.toLocaleString()}`, WIDTH / 2, boxY + 475);
      } else {
        ctx.fillStyle = '#c8d4f0';
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.fillText("CATCH FALLING CAKES - DODGE ANVILS!", WIDTH / 2, boxY + 396);

        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '14px "Press Start 2P", monospace';
        ctx.fillText("▶ TAP SCREEN TO PLAY ◀", WIDTH / 2, boxY + 440);

        ctx.fillStyle = '#859bb8';
        ctx.font = '9px "Press Start 2P", monospace';
        ctx.fillText("BEST: " + hiScore.toLocaleString() + "   |   TAP ARROWS OR GLIDE THUMB", WIDTH / 2, boxY + 485);
      }
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
      // Cosmic Hyperdrive Warp Transition Effect
      ctx.save();
      const warpProgress = 1.0 - (stageClearTime / 1.8);
      ctx.fillStyle = 'rgba(8, 4, 26, 0.55)';
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      ctx.translate(WIDTH / 2, HEIGHT / 2);
      for (let i = 0; i < 44; i++) {
        const angle = (i / 44) * Math.PI * 2 + globalTime * 0.6;
        const r1 = 20 + warpProgress * 90;
        const r2 = r1 + 80 + warpProgress * 520;
        ctx.strokeStyle = i % 2 === 0 ? '#00dcff' : '#ff4da6';
        ctx.lineWidth = 2.5 + Math.sin(i) * 1.0;
        ctx.shadowColor = i % 2 === 0 ? '#00dcff' : '#ff4da6';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.moveTo(Math.cos(angle) * r1, Math.sin(angle) * r1);
        ctx.lineTo(Math.cos(angle) * r2, Math.sin(angle) * r2);
        ctx.stroke();
      }
      ctx.restore();

      ctx.fillStyle = COLORS.GOLD;
      ctx.shadowColor = COLORS.GOLD;
      ctx.shadowBlur = 16;
      ctx.font = '22px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("STAGE " + stage + " CLEAR!", WIDTH / 2, HEIGHT / 2 - 25);
      ctx.fillStyle = COLORS.CYAN;
      ctx.shadowColor = COLORS.CYAN;
      ctx.shadowBlur = 12;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("WARPING TO LEVEL " + (stage + 1) + "...", WIDTH / 2, HEIGHT / 2 + 35);
      ctx.shadowBlur = 0;
    } else if (state === 'CANDLE_CEREMONY') {
      const boxW = Math.min(WIDTH - 24, 670);
      const boxH = Math.min(HEIGHT - 80, 560);
      const boxX = WIDTH / 2 - boxW / 2;
      const boxY = HEIGHT / 2 - boxH / 2;

      // Dark Cosmic Card Backdrop
      ctx.fillStyle = 'rgba(12, 6, 36, 0.96)';
      ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.strokeStyle = COLORS.GOLD;
      ctx.lineWidth = 4;
      ctx.strokeRect(boxX, boxY, boxW, boxH);

      // Gold Corner Accent Pixels
      ctx.fillStyle = COLORS.CYAN;
      [[boxX, boxY], [boxX + boxW - 12, boxY], [boxX, boxY + boxH - 12], [boxX + boxW - 12, boxY + boxH - 12]].forEach(([cxo, cyo]) => {
        ctx.fillRect(cxo, cyo, 12, 12);
      });

      const info = MILESTONE_MESSAGES[stage] || {
        title: "★ AISHA'S BIRTHDAY WISH! ★",
        sub: "HAPPY BIRTHDAY AISHA! 🎂",
        note: `STAGE ${stage} MASTERED! MAKE A WISH!`,
        bonus: "+1,000 WISH BONUS AWARDED"
      };

      // Header Banner
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '16px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(info.title, WIDTH / 2, boxY + 34);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText(info.sub, WIDTH / 2, boxY + 58);

      // Aisha Floating Portrait Centerpiece
      const floatY = Math.sin(globalTime * 2.2) * 4;
      drawAishaPortrait(ctx, WIDTH / 2, boxY + 145, 120, 150, floatY);

      // Interactive Birthday Cake in Ceremony
      const cakeBaseY = boxY + 395;
      // Tier 1 Base Layer
      ctx.fillStyle = '#ff4da6';
      ctx.fillRect(WIDTH / 2 - 120, cakeBaseY - 45, 240, 45);
      ctx.fillStyle = '#00dcff';
      for (let cx = WIDTH / 2 - 120; cx < WIDTH / 2 + 120; cx += 16) {
        ctx.beginPath(); ctx.arc(cx + 8, cakeBaseY, 8, Math.PI, 0); ctx.fill();
      }
      ctx.fillStyle = '#ffffff';
      for (let cx = WIDTH / 2 - 100; cx < WIDTH / 2 + 100; cx += 25) {
        ctx.fillRect(cx, cakeBaseY - 32, 6, 6);
      }

      // Tier 2 Middle Layer
      ctx.fillStyle = '#f4a261';
      ctx.fillRect(WIDTH / 2 - 95, cakeBaseY - 85, 190, 40);
      ctx.fillStyle = '#fff3b0';
      ctx.fillRect(WIDTH / 2 - 95, cakeBaseY - 78, 190, 8);
      ctx.fillStyle = '#ff4da6';
      for (let cx = WIDTH / 2 - 95; cx < WIDTH / 2 + 95; cx += 16) {
        ctx.beginPath(); ctx.arc(cx + 8, cakeBaseY - 45, 7, Math.PI, 0); ctx.fill();
      }

      // Tier 3 Top Layer
      ctx.fillStyle = '#c040ff';
      ctx.fillRect(WIDTH / 2 - 70, cakeBaseY - 120, 140, 35);
      ctx.fillStyle = '#00dcff';
      ctx.fillRect(WIDTH / 2 - 70, cakeBaseY - 114, 140, 6);

      // Render 5 Interactive Birthday Candles on the Cake
      const candleY = cakeBaseY - 120;
      ceremonyCandles.forEach(c => {
        c.y = candleY;
        ctx.fillStyle = c.color;
        ctx.fillRect(c.x - 4, c.y - 24, 8, 24);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(c.x - 4, c.y - 18, 8, 3);
        ctx.fillRect(c.x - 4, c.y - 8, 8, 3);
        ctx.strokeStyle = '#222';
        ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(c.x, c.y - 24); ctx.lineTo(c.x, c.y - 30); ctx.stroke();

        if (c.lit) {
          const fl = Math.sin(globalTime * 18 + c.flicker) * 2;
          ctx.fillStyle = 'rgba(255, 160, 0, 0.45)';
          ctx.beginPath(); ctx.arc(c.x, c.y - 38 + fl * 0.5, 9, 0, Math.PI * 2); ctx.fill();

          ctx.fillStyle = '#ff7700';
          ctx.beginPath();
          ctx.moveTo(c.x, c.y - 45 + fl);
          ctx.quadraticCurveTo(c.x - 6, c.y - 36, c.x, c.y - 30);
          ctx.quadraticCurveTo(c.x + 6, c.y - 36, c.x, c.y - 45 + fl);
          ctx.fill();

          ctx.fillStyle = '#ffea00';
          ctx.beginPath();
          ctx.moveTo(c.x, c.y - 41 + fl * 0.7);
          ctx.quadraticCurveTo(c.x - 3, c.y - 35, c.x, c.y - 31);
          ctx.quadraticCurveTo(c.x + 3, c.y - 35, c.x, c.y - 41 + fl * 0.7);
          ctx.fill();
        }
      });

      // Smoke particles from blown candles
      ceremonySmokeParticles.forEach(sp => {
        ctx.save();
        ctx.fillStyle = `rgba(215, 220, 235, ${sp.alpha * 0.75})`;
        ctx.beginPath();
        ctx.arc(sp.x, sp.y, sp.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });

      // Ceremony Status & Instructions
      if (!ceremonyAllBlown) {
        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '11px "Press Start 2P", monospace';
        ctx.fillText("🎂 TAP CANDLES OR BLOW PHONE MIC! 🎂", WIDTH / 2, boxY + 445);

        if (!micEnabled) {
          ctx.fillStyle = '#37be46';
          ctx.font = '9px "Press Start 2P", monospace';
          ctx.fillText("🎤 [ TAP 'BLOW MIC' TO USE REAL BREATH! ]", WIDTH / 2, boxY + 475);
        } else {
          ctx.fillStyle = '#37be46';
          ctx.font = '9px "Press Start 2P", monospace';
          ctx.fillText("🎤 MIC ACTIVE — BLOW INTO MIC NOW! 💨", WIDTH / 2, boxY + 468);

          const mBarW = 160;
          const mBarH = 8;
          const mBarX = WIDTH / 2 - mBarW / 2;
          const mBarY = boxY + 478;
          ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
          ctx.fillRect(mBarX, mBarY, mBarW, mBarH);
          ctx.fillStyle = micBlowLevel > 0.4 ? '#00f0ff' : '#37be46';
          ctx.fillRect(mBarX, mBarY, mBarW * micBlowLevel, mBarH);
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 1;
          ctx.strokeRect(mBarX, mBarY, mBarW, mBarH);
        }
      } else {
        ctx.fillStyle = COLORS.GOLD;
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.fillText("★ BIRTHDAY WISH GRANTED! ★", WIDTH / 2, boxY + 425);

        ctx.fillStyle = '#ffffff';
        ctx.font = '9px "Press Start 2P", monospace';
        ctx.fillText(info.note, WIDTH / 2, boxY + 450);

        const advPrompt = (stage < TOTAL_STAGES) ? `▶ TAP TO ADVANCE TO LEVEL ${stage + 1} ◀` : "★ TAP TO PLAY AGAIN ★";
        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '12px "Press Start 2P", monospace';
        ctx.fillText(advPrompt, WIDTH / 2, boxY + 480);

        ctx.fillStyle = '#ff6ebe';
        ctx.font = '9px "Press Start 2P", monospace';
        ctx.fillText("📸 [ TAP HERE TO SHARE POLAROID CERTIFICATE ]", WIDTH / 2, boxY + 508);

        ctx.fillStyle = '#859bb8';
        ctx.font = '8px "Press Start 2P", monospace';
        ctx.fillText(`${info.bonus}   |   SCORE: ${score.toLocaleString()}`, WIDTH / 2, boxY + 532);
      }
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
      ctx.fillText("★ GRAND CHAMPION BAKER! ★", WIDTH / 2, boxY + 36);

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
      ctx.fillText("★ ALL 30 LEVELS CONQUERED! ★", WIDTH / 2, portY + portH / 2 + 22 + floatY);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '12px "Press Start 2P", monospace';
      ctx.fillText("FINAL SCORE: " + score.toLocaleString(), WIDTH / 2, boxY + 396);

      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("★ TAP TO PLAY AGAIN ★", WIDTH / 2, boxY + 434);

      ctx.fillStyle = '#ff6ebe';
      ctx.font = '10px "Press Start 2P", monospace';
      ctx.fillText("📸 TAP TO SHARE POLAROID CERTIFICATE 📸", WIDTH / 2, boxY + 468);

      ctx.fillStyle = '#859bb8';
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.fillText("BEST: " + hiScore.toLocaleString(), WIDTH / 2, boxY + 500);
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
