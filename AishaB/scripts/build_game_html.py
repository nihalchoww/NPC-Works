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
<meta name="apple-mobile-web-app-title" content="Aisha Bake-Off">
<meta name="application-name" content="Aisha Bake-Off">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#ff3388">
<title>Aisha's Birthday Bake-Off 🎂</title>
<link rel="manifest" href="/manifest.json">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="apple-touch-icon-precomposed" href="/apple-touch-icon.png">
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
    width: 100%;
    height: 100%;
    height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(ellipse at center, #1b1248 0%, #0d0824 60%, #060312 100%);
    overflow: hidden;
  }
  canvas {
    width: 100%;
    height: 100%;
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

  /* Quick Settings Collapsible Dock (Option 1) */
  #settings-dock-wrap {
    position: absolute;
    top: max(14px, env(safe-area-inset-top));
    left: max(14px, env(safe-area-inset-left));
    z-index: 30;
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: none;
  }
  #gear-btn {
    position: static;
    pointer-events: auto;
    font-size: 19px;
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.15s ease, border-color 0.15s ease;
  }
  #gear-btn.open {
    transform: rotate(60deg) scale(1.08);
    background: rgba(255, 77, 166, 0.45);
    border-color: #ff3388;
    color: #ffd700;
    box-shadow: 0 0 18px rgba(255, 51, 136, 0.7);
  }
  #settings-dock {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(13, 7, 34, 0.92);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 3px 8px;
    border-radius: 16px;
    border: 1.5px solid rgba(0, 220, 255, 0.5);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.85), 0 0 16px rgba(0, 220, 255, 0.3);
    pointer-events: auto;
    transition: opacity 0.22s ease, transform 0.22s cubic-bezier(0.34, 1.3, 0.64, 1);
    transform-origin: left center;
  }
  #settings-dock.collapsed {
    opacity: 0;
    pointer-events: none;
    transform: scale(0.65) translateX(-14px);
  }
  .dock-btn {
    background: rgba(22, 32, 70, 0.75);
    border: 1px solid rgba(0, 220, 255, 0.4);
    color: #ffffff;
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    cursor: pointer;
    touch-action: manipulation;
    transition: all 0.15s ease;
    box-shadow: 0 0 8px rgba(0, 220, 255, 0.15);
  }
  .dock-btn:active {
    background: rgba(0, 220, 255, 0.45);
    transform: scale(0.92);
  }
  .dock-btn.active, #tilt-btn.active {
    background: rgba(0, 220, 255, 0.45);
    border-color: #ffd700;
    color: #ffd700;
    box-shadow: 0 0 14px rgba(0, 220, 255, 0.8), inset 0 0 6px #ffd700;
  }
  #pwa-btn.installed {
    border-color: #00ff88;
    color: #00ff88;
    box-shadow: 0 0 12px rgba(0, 255, 136, 0.4);
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
  /* Floating Microphone Button for Candle Ceremony */
  #btn-mic {
    position: absolute;
    top: max(12px, env(safe-area-inset-top));
    right: calc(max(12px, env(safe-area-inset-right)) + 58px);
    z-index: 25;
    display: none;
    font-size: 20px;
    border-color: #37be46;
    color: #37be46;
    box-shadow: 0 0 14px rgba(55, 190, 70, 0.4);
    transition: all 0.2s ease;
  }
  #btn-mic.active {
    background: rgba(55, 190, 70, 0.45);
    border-color: #00ff88;
    color: #ffffff;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.85), inset 0 0 10px #00ff88;
  }
  /* Shareable Victory Polaroid Purikura Certificate Modal */
  #polaroid-modal {
    display: none;
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    background: rgba(6, 3, 18, 0.95);
    z-index: 100;
    align-items: center;
    justify-content: flex-start;
    flex-direction: column;
    padding: 12px 10px;
    box-sizing: border-box;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
  #polaroid-wrap {
    max-width: 400px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 7px;
    margin: auto 0;
  }
  .purikura-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
  }
  .purikura-badge {
    background: linear-gradient(135deg, #ff007f, #9b5de5);
    color: #ffffff;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    padding: 5px 12px;
    border-radius: 20px;
    box-shadow: 0 0 14px rgba(255, 0, 127, 0.5);
    letter-spacing: 0.5px;
  }
  .photo-switcher-bar {
    display: flex;
    gap: 6px;
    width: 100%;
    max-width: 320px;
    justify-content: center;
  }
  .photo-tab-btn {
    flex: 1;
    padding: 6px 3px;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    border-radius: 8px;
    border: 1.5px solid #ff4da6;
    background: rgba(255, 77, 166, 0.15);
    color: #fff;
    cursor: pointer;
    transition: all 0.15s ease;
  }
  .photo-tab-btn.active {
    background: linear-gradient(135deg, #ff007f, #ffd700);
    color: #000;
    font-weight: bold;
    border-color: #ffd700;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.5);
  }
  #polaroid-canvas {
    width: 100%;
    max-width: 310px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9), 0 0 20px rgba(255, 215, 0, 0.35);
    display: block;
    touch-action: none;
    cursor: grab;
    user-select: none;
    -webkit-user-select: none;
  }
  #polaroid-canvas:active {
    cursor: grabbing;
  }
  /* Purikura Sticker Toolbar */
  .sticker-toolbar-wrap {
    width: 100%;
    max-width: 320px;
    background: rgba(18, 10, 40, 0.95);
    border: 1.5px solid #ff4da6;
    border-radius: 10px;
    padding: 7px 8px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    box-shadow: 0 0 14px rgba(255, 77, 166, 0.25);
  }
  .sticker-tray {
    display: flex;
    gap: 5px;
    overflow-x: auto;
    width: 100%;
    padding: 3px 2px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }
  .sticker-tray::-webkit-scrollbar {
    display: none;
  }
  .sticker-btn {
    min-width: 36px;
    height: 36px;
    font-size: 19px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.08);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: transform 0.1s ease;
  }
  .sticker-btn:active {
    transform: scale(1.25);
  }
  .sticker-actions-row {
    display: flex;
    gap: 8px;
    width: 100%;
    justify-content: center;
  }
  .sticker-util-btn {
    padding: 4px 7px;
    font-family: 'Press Start 2P', monospace;
    font-size: 6.5px;
    border-radius: 6px;
    border: 1px solid #00dcff;
    background: rgba(0, 220, 255, 0.15);
    color: #00dcff;
    cursor: pointer;
  }
  .sticker-util-btn:hover {
    background: rgba(0, 220, 255, 0.3);
  }
  /* Custom Wish Box in Polaroid Modal */
  .polaroid-wish-box {
    margin-top: 3px;
    width: 100%;
    max-width: 320px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .wish-input-row {
    display: flex;
    gap: 5px;
    width: 100%;
    margin-top: 4px;
  }
  #polaroid-wish-input {
    flex: 1;
    background: #0f0826;
    border: 1.5px solid #00dcff;
    color: #ffd700;
    padding: 7px 8px;
    border-radius: 8px;
    font-family: 'Press Start 2P', monospace;
    font-size: 7.5px;
    outline: none;
    box-shadow: inset 0 0 8px rgba(0, 220, 255, 0.2);
  }
  #polaroid-wish-input:focus {
    border-color: #ffd700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  }
  .wish-apply-btn {
    background: #ffd700;
    color: #000;
    border: none;
    border-radius: 8px;
    padding: 7px 9px;
    font-family: 'Press Start 2P', monospace;
    font-size: 7.5px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
  }
  .wish-chips {
    display: flex;
    gap: 5px;
    margin-top: 4px;
    flex-wrap: wrap;
    justify-content: center;
  }
  .wish-chip {
    background: rgba(255, 77, 166, 0.2);
    border: 1px solid #ff4da6;
    color: #ffb3c6;
    border-radius: 12px;
    padding: 4px 7px;
    font-size: 6.5px;
    cursor: pointer;
    transition: all 0.1s ease;
  }
  .wish-chip:active {
    background: #ff4da6;
    color: #fff;
    transform: scale(0.95);
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
  /* Progressive Web App (PWA) Install Modal */
  #pwa-modal {
    display: none;
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    background: rgba(6, 3, 18, 0.94);
    z-index: 120;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 16px;
    box-sizing: border-box;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  #pwa-wrap {
    max-width: 90vw;
    width: 380px;
    max-height: 88dvh;
    background: #0d0722;
    border: 2px solid #ff3388;
    border-radius: 16px;
    padding: 20px 16px;
    box-shadow: 0 0 30px rgba(255, 51, 136, 0.4), inset 0 0 20px rgba(0, 220, 255, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;
    overflow-y: auto;
  }
  .pwa-badge {
    background: #ff3388;
    color: #fff;
    font-size: 8px;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 10px;
    margin-bottom: 10px;
  }
  #pwa-icon-preview {
    width: 80px;
    height: 80px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 15px rgba(255, 215, 0, 0.5);
    border: 2px solid #ffd700;
  }
  .pwa-points {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    margin-top: 8px;
    font-size: 7.5px;
    line-height: 1.5;
    color: #d1c4e9;
  }
  .pwa-point {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    background: rgba(255, 255, 255, 0.04);
    padding: 8px;
    border-radius: 8px;
    border: 1px solid rgba(255, 51, 136, 0.2);
  }
  .pwa-point-icon {
    font-size: 14px;
    line-height: 1;
  }
  .pwa-ios-guide {
    background: rgba(0, 220, 255, 0.1);
    border: 1px dashed #00dcff;
    padding: 10px;
    border-radius: 10px;
    font-size: 7.5px;
    line-height: 1.6;
    color: #00dcff;
    text-align: left;
    margin-top: 10px;
    width: 100%;
    box-sizing: border-box;
  /* ─── RETRO ARCADE HIGH SCORE INITIALS MODAL ───────────────────────── */
  #initials-modal {
    display: none;
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100dvh;
    background: rgba(6, 3, 18, 0.95);
    z-index: 130;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 12px;
    box-sizing: border-box;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
  #initials-wrap {
    max-width: 380px;
    width: 94%;
    background: #0d0722;
    border: 2.5px solid #ffd700;
    border-radius: 16px;
    padding: 16px 14px;
    box-shadow: 0 0 35px rgba(255, 215, 0, 0.4), inset 0 0 20px rgba(255, 0, 127, 0.2);
    display: flex;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;
    text-align: center;
    margin: auto;
  }
  .initials-badge {
    background: linear-gradient(135deg, #ffd700, #ff8800);
    color: #000;
    font-size: 8px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 5px 12px;
    border-radius: 12px;
    box-shadow: 0 0 14px rgba(255, 215, 0, 0.5);
  }
  .initials-slots {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 12px 0 8px 0;
  }
  .initial-slot {
    width: 44px;
    height: 52px;
    border: 2.5px solid #00dcff;
    border-radius: 8px;
    background: rgba(0, 220, 255, 0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-family: 'Press Start 2P', monospace;
    color: #ffffff;
    box-shadow: inset 0 0 8px rgba(0, 220, 255, 0.3);
    transition: all 0.15s ease;
  }
  .initial-slot.active {
    border-color: #ffd700;
    background: rgba(255, 215, 0, 0.22);
    box-shadow: 0 0 16px rgba(255, 215, 0, 0.6), inset 0 0 8px #ffd700;
    animation: slotBlink 1s infinite alternate;
  }
  @keyframes slotBlink {
    0% { transform: scale(1); border-color: #ffd700; }
    100% { transform: scale(1.04); border-color: #ff007f; }
  }
  .quick-initials-row {
    margin: 6px 0 10px 0;
    width: 100%;
  }
  .quick-initials-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: center;
  }
  .quick-chip {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 215, 0, 0.5);
    color: #ffd700;
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    padding: 5px 8px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.12s ease;
  }
  .quick-chip:active {
    background: #ffd700;
    color: #000;
    transform: scale(0.94);
  }
  .arcade-keypad {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 100%;
    max-width: 330px;
    margin: 4px auto 0;
  }
  .keypad-row {
    display: flex;
    gap: 3px;
    justify-content: center;
  }
  .arcade-key {
    flex: 1;
    min-width: 25px;
    height: 30px;
    background: #182245;
    border: 1px solid #36497f;
    color: #ffffff;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.1s ease;
    user-select: none;
    -webkit-user-select: none;
  }
  .arcade-key:active {
    background: #ff007f;
    border-color: #ffd700;
    color: #ffffff;
    transform: scale(0.92);
  }

  /* ─── RETRO ARCADE HALL OF FAME RECTANGULAR POP-UP WINDOW ───────────── */
  #leaderboard-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    background: rgba(4, 2, 14, 0.88);
    z-index: 999999;
    align-items: center;
    justify-content: center;
    padding: 16px;
    box-sizing: border-box;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    touch-action: none;
  }
  #leaderboard-wrap {
    position: relative;
    max-width: 330px;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    margin-top: auto;
    margin-bottom: auto;
    background: #0d0824;
    border: 2.5px solid #00dcff;
    border-radius: 14px;
    padding: 20px 14px 14px 14px;
    box-shadow: 0 0 45px rgba(0, 220, 255, 0.55), 0 15px 45px rgba(0, 0, 0, 0.95);
    display: flex;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;
    text-align: center;
    animation: popupBoxOpen 0.22s cubic-bezier(0.18, 0.89, 0.32, 1.28);
  }
  @keyframes popupBoxOpen {
    0% { transform: scale(0.85); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
  }
  .leaderboard-close-x, .mini-close-x {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: 2px solid #ff3388;
    background: #ff007f;
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 0 14px rgba(255, 0, 127, 0.6);
    touch-action: manipulation;
    z-index: 10;
    transition: all 0.15s ease;
  }
  .leaderboard-close-x:hover, .leaderboard-close-x:active,
  .mini-close-x:hover, .mini-close-x:active {
    background: #ff3388;
    border-color: #ffd700;
    transform: scale(1.12);
  }
  .leaderboard-badge {
    background: linear-gradient(135deg, #00dcff, #9b5de5);
    color: #000;
    font-size: 7.5px;
    font-weight: bold;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 220, 255, 0.4);
  }
  .leaderboard-table {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin: 8px 0;
  }
  .lb-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.04);
    border: 1.5px solid rgba(0, 220, 255, 0.25);
    border-radius: 8px;
    padding: 6px 8px;
    box-sizing: border-box;
    transition: all 0.2s ease;
  }
  .lb-row.rank-1 {
    border-color: #ffd700;
    background: linear-gradient(90deg, rgba(255, 215, 0, 0.2), rgba(255, 77, 166, 0.1));
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.3);
  }
  .lb-row.rank-2 {
    border-color: #d1d5db;
    background: linear-gradient(90deg, rgba(209, 213, 219, 0.15), rgba(60, 80, 140, 0.1));
  }
  .lb-row.rank-3 {
    border-color: #cd7f32;
    background: linear-gradient(90deg, rgba(205, 127, 50, 0.18), rgba(80, 40, 20, 0.1));
  }
  .lb-row.new-entry-glow {
    border-color: #00ff88;
    background: linear-gradient(90deg, rgba(0, 255, 136, 0.25), rgba(0, 220, 255, 0.15));
    box-shadow: 0 0 16px rgba(0, 255, 136, 0.6);
  }
  .lb-left {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .lb-trophy {
    font-size: 13px;
    line-height: 1;
    width: 18px;
    text-align: center;
  }
  .lb-name {
    font-family: 'Press Start 2P', monospace;
    font-size: 8.5px;
    color: #ffffff;
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  .lb-stage-tag {
    font-size: 6px;
    color: #ff94c2;
    background: rgba(255, 77, 166, 0.2);
    padding: 1px 4px;
    border-radius: 4px;
    border: 1px solid rgba(255, 77, 166, 0.35);
  }
  .lb-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 1px;
  }
  .lb-score {
    font-family: 'Press Start 2P', monospace;
    font-size: 8.5px;
    color: #ffd700;
  }
  .lb-date {
    font-size: 5.5px;
    color: #859bb8;
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
  <div id="settings-dock-wrap">
    <button class="hud-btn" id="gear-btn" title="Quick Settings ⚙️" aria-label="Quick Settings">⚙️</button>
    <div id="settings-dock" class="collapsed">
      <button class="dock-btn" id="leaderboard-btn" title="🏆 Hall of Fame Leaderboard">🏆</button>
      <button class="dock-btn" id="mute-btn" title="Toggle Sound">🔊</button>
      <button class="dock-btn" id="tilt-btn" title="Toggle Phone Tilt / Gyroscope Steering">📳</button>
      <button class="dock-btn" id="crt-btn" title="Toggle CRT Arcade Cabinet Mode">📺</button>
      <button class="dock-btn" id="fs-btn" title="Toggle Fullscreen">⛶</button>
      <button class="dock-btn" id="pwa-btn" title="Add to Home Screen / Install Native App">📱</button>
    </div>
  </div>
  <button class="hud-btn" id="pause-btn" title="Pause / Resume">⏸</button>
  <button class="hud-btn" id="btn-mic" title="Blow candles with microphone" aria-label="Microphone">🎤</button>
  <div id="polaroid-modal">
    <div id="polaroid-wrap">
      <div class="purikura-header">
        <div class="purikura-badge">📸 PURIKURA PHOTO BOOTH</div>
        <div style="font-size: 7.5px; color: #ffd700;">★ DECORATE AISHA'S BIRTHDAY CARD ★</div>
      </div>

      <div class="photo-switcher-bar">
        <button class="photo-tab-btn active" id="tab-portrait" data-photo="portrait">👑 Portrait</button>
        <button class="photo-tab-btn" id="tab-candid" data-photo="candid">🥤 Candid</button>
        <button class="photo-tab-btn" id="tab-pixel" data-photo="pixel">👾 Pixel-Art</button>
      </div>

      <canvas id="polaroid-canvas" width="640" height="880"></canvas>

      <div class="sticker-toolbar-wrap">
        <div style="font-size: 7px; color: #ff6ebe; letter-spacing: 0.5px;">✨ TAP STICKERS TO STAMP (DRAG TO MOVE):</div>
        <div class="sticker-tray">
          <button class="sticker-btn" data-sticker="👑" title="Birthday Crown">👑</button>
          <button class="sticker-btn" data-sticker="🎀" title="Pink Bow">🎀</button>
          <button class="sticker-btn" data-sticker="🎈" title="Balloons">🎈</button>
          <button class="sticker-btn" data-sticker="✨" title="Sparkles">✨</button>
          <button class="sticker-btn" data-sticker="💖" title="Heart">💖</button>
          <button class="sticker-btn" data-sticker="🍰" title="Cupcake">🍰</button>
          <button class="sticker-btn" data-sticker="🐱" title="Cute Cat Ears">🐱</button>
          <button class="sticker-btn" data-sticker="🎉" title="Party Popper">🎉</button>
          <button class="sticker-btn" data-sticker="⭐" title="Gold Star">⭐</button>
          <button class="sticker-btn" data-sticker="🍓" title="Strawberry">🍓</button>
          <button class="sticker-btn" data-sticker="🌸" title="Flower">🌸</button>
          <button class="sticker-btn" data-sticker="🍭" title="Lollipop">🍭</button>
        </div>
        <div class="sticker-actions-row">
          <button class="sticker-util-btn" id="sticker-undo-btn">↺ REMOVE LAST</button>
          <button class="sticker-util-btn" id="sticker-clear-btn">✕ CLEAR ALL</button>
        </div>
      </div>

      <div class="polaroid-wish-box">
        <label for="polaroid-wish-input" style="font-size: 7.5px; color: #ff6ebe; letter-spacing: 1px;">💌 WRITE YOUR WISH FOR AISHA:</label>
        <div class="wish-input-row">
          <input type="text" id="polaroid-wish-input" maxlength="34" placeholder="Happy Birthday Aisha! 🎂" value="Happy Birthday Aisha! 🎂" />
          <button id="polaroid-wish-btn" class="wish-apply-btn">UPDATE ✨</button>
        </div>
        <div class="wish-chips">
          <span class="wish-chip" data-wish="Queen of the Galaxy Bakery! 👑">👑 Queen Baker</span>
          <span class="wish-chip" data-wish="May your year be 100x sweeter! 🍰">🍰 100x Sweeter</span>
          <span class="wish-chip" data-wish="Endless joy, love & laughter! 💖">💖 Endless Joy</span>
        </div>
      </div>

      <p style="font-size: 7.5px; color: #ffd700; margin: 4px 0; text-align: center; text-shadow: 0 0 8px #000;">★ TAP &amp; DRAG STICKERS • READY TO SHARE ★</p>

      <div class="modal-actions" style="margin-top: 4px;">
        <button class="modal-btn" id="modal-share-btn" style="background:#ff007f; color:#fff;">SHARE 💌</button>
        <button class="modal-btn" id="modal-download-btn">DOWNLOAD 📥</button>
        <button class="modal-btn modal-btn-close" id="modal-close-btn">CLOSE ✕</button>
      </div>
    </div>
  </div>
  <div id="pwa-modal">
    <div id="pwa-wrap">
      <div class="pwa-badge">📱 PROGRESSIVE WEB APP</div>
      <img src="data:image/png;base64,%%AISHA_ICON_B64%%" alt="Aisha Bake-Off Icon" id="pwa-icon-preview" />
      <h3 style="font-size: 11px; color: #ffd700; margin: 10px 0 6px 0; text-align: center;">AISHA'S BIRTHDAY BAKE-OFF</h3>
      <p style="font-size: 8px; color: #ff6ebe; text-align: center; margin-bottom: 12px;">★ Full Native App Experience ★</p>

      <div class="pwa-points">
        <div class="pwa-point">
          <span class="pwa-point-icon">⚡</span>
          <div><b>True Fullscreen Native:</b> Opens edge-to-edge without browser address bar, URL arrows, or Safari toolbars.</div>
        </div>
        <div class="pwa-point">
          <span class="pwa-point-icon">✈️</span>
          <div><b>100% Offline Playable:</b> Service Worker caching allows full play on airplanes or subway with zero Wi-Fi!</div>
        </div>
        <div class="pwa-point">
          <span class="pwa-point-icon">🧁</span>
          <div><b>Custom Aisha App Icon:</b> Official home screen icon with Aisha's party hat &amp; butterfly clip!</div>
        </div>
      </div>

      <div id="pwa-prompt-container" style="width: 100%; text-align: center; margin-top: 14px;"></div>

      <div class="modal-actions" style="margin-top: 16px;">
        <button class="modal-btn" id="pwa-action-btn" style="display:none;">INSTALL APP 📲</button>
        <button class="modal-btn modal-btn-close" id="pwa-close-btn">BACK TO GAME ✕</button>
      </div>
    </div>
  </div>

  <!-- Retro Arcade High Score Name Entry Modal -->
  <div id="initials-modal">
    <div id="initials-wrap">
      <button class="mini-close-x" id="initials-close-x" title="Skip">✕</button>
      <div class="initials-badge">★ NEW HIGH SCORE! ★</div>
      <h3 style="font-size: 11px; color: #ffd700; margin: 8px 0 3px 0; text-align: center;" id="initials-rank-title">TOP 5 BAKER: RANK #1!</h3>
      <div style="font-size: 14px; color: #00dcff; font-family: 'Press Start 2P', monospace; margin-bottom: 8px;" id="initials-score-text">28,500 PTS</div>
      <p style="font-size: 7.5px; color: #ff6ebe; margin: 0 0 10px 0; line-height: 1.4;">ENTER YOUR 3-LETTER INITIALS FOR THE ARCADE BOARD:</p>

      <div class="initials-slots" id="initials-slots">
        <span class="initial-slot active" id="slot-0">A</span>
        <span class="initial-slot" id="slot-1">S</span>
        <span class="initial-slot" id="slot-2">H</span>
      </div>

      <input type="text" id="initials-input" maxlength="3" autocomplete="off" autocapitalize="characters" style="position:absolute; opacity:0; pointer-events:none;" />

      <div class="quick-initials-row">
        <div style="font-size: 6.5px; color: #859bb8; margin-bottom: 4px;">QUICK PICK INITIALS:</div>
        <div class="quick-initials-chips">
          <button class="quick-chip" data-initials="ASH">👑 ASH</button>
          <button class="quick-chip" data-initials="MOM">💖 MOM</button>
          <button class="quick-chip" data-initials="DAD">⭐ DAD</button>
          <button class="quick-chip" data-initials="BFF">🍰 BFF</button>
          <button class="quick-chip" data-initials="SIS">🎀 SIS</button>
          <button class="quick-chip" data-initials="CAT">🐱 CAT</button>
        </div>
      </div>

      <div class="arcade-keypad" id="arcade-keypad">
        <div class="keypad-row">
          <button class="arcade-key" data-char="A">A</button><button class="arcade-key" data-char="B">B</button><button class="arcade-key" data-char="C">C</button><button class="arcade-key" data-char="D">D</button><button class="arcade-key" data-char="E">E</button><button class="arcade-key" data-char="F">F</button><button class="arcade-key" data-char="G">G</button><button class="arcade-key" data-char="H">H</button><button class="arcade-key" data-char="I">I</button>
        </div>
        <div class="keypad-row">
          <button class="arcade-key" data-char="J">J</button><button class="arcade-key" data-char="K">K</button><button class="arcade-key" data-char="L">L</button><button class="arcade-key" data-char="M">M</button><button class="arcade-key" data-char="N">N</button><button class="arcade-key" data-char="O">O</button><button class="arcade-key" data-char="P">P</button><button class="arcade-key" data-char="Q">Q</button><button class="arcade-key" data-char="R">R</button>
        </div>
        <div class="keypad-row">
          <button class="arcade-key" data-char="S">S</button><button class="arcade-key" data-char="T">T</button><button class="arcade-key" data-char="U">U</button><button class="arcade-key" data-char="V">V</button><button class="arcade-key" data-char="W">W</button><button class="arcade-key" data-char="X">X</button><button class="arcade-key" data-char="Y">Y</button><button class="arcade-key" data-char="Z">Z</button><button class="arcade-key" data-char="★">★</button>
        </div>
        <div class="keypad-row">
          <button class="arcade-key" data-char="0">0</button><button class="arcade-key" data-char="1">1</button><button class="arcade-key" data-char="2">2</button><button class="arcade-key" data-char="3">3</button><button class="arcade-key" data-char="4">4</button><button class="arcade-key" data-char="5">5</button><button class="arcade-key" data-char="6">6</button><button class="arcade-key" data-char="7">7</button><button class="arcade-key" data-char="8">8</button><button class="arcade-key" data-char="9">9</button><button class="arcade-key" id="key-backspace" title="Backspace">⌫</button>
        </div>
      </div>

      <div class="modal-actions" style="margin-top: 12px;">
        <button class="modal-btn" id="initials-submit-btn" style="background: linear-gradient(135deg, #ffd700, #ff8800); color: #000; font-weight: bold;">SUBMIT 🏆</button>
        <button class="modal-btn modal-btn-close" id="initials-skip-btn">SKIP ✕</button>
      </div>
    </div>
  </div>
</div>

<!-- Retro Arcade Hall of Fame Leaderboard Modal (Separate Rectangular Pop-Up Window) -->
<div id="leaderboard-modal">
  <div id="leaderboard-wrap">
    <button class="leaderboard-close-x" id="lb-close-x" title="Exit Leaderboard (Resume Game)" aria-label="Exit">✕</button>
    <div class="leaderboard-badge">🏆 RETRO ARCADE</div>
    <h3 style="font-size: 11px; color: #ffd700; margin: 6px 0 2px 0; text-align: center;">HALL OF FAME</h3>
    <p style="font-size: 7px; color: #ff6ebe; margin: 0 0 8px 0; text-align: center;">★ TOP 5 GALAXY BAKERS ★</p>

    <div class="leaderboard-table" id="leaderboard-table">
      <!-- Rendered dynamically -->
    </div>

    <div id="leaderboard-current-stat" style="font-size: 6.5px; color: #859bb8; margin-top: 5px; font-family: 'Press Start 2P', monospace;">
      CURRENT RUN: 0 PTS
    </div>

    <div class="modal-actions" style="margin-top: 10px; gap: 6px;">
      <button class="modal-btn" id="lb-share-btn" style="background:#ff007f; color:#fff; font-size: 7.5px; padding: 5px 8px;">SHARE 📲</button>
      <button class="modal-btn" id="lb-reset-btn" style="background:#223366; font-size: 7px; padding: 5px 6px;">RESET ↺</button>
      <button class="modal-btn modal-btn-close" id="lb-close-btn" style="font-size: 7.5px; padding: 5px 8px;">EXIT ✕</button>
    </div>
  </div>
</div>

<script>
(() => {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  // Load Aisha Portrait, Candid & Head Sprites
  const aishaPortrait = new Image();
  aishaPortrait.src = "data:image/jpeg;base64,%%AISHA_PORTRAIT_B64%%";

  const aishaCandid = new Image();
  aishaCandid.src = "data:image/jpeg;base64,%%AISHA_CANDID_B64%%";

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
  function sfxStarFever() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    const starNotes = [523, 659, 784, 1046, 1318, 1568];
    starNotes.forEach((f, i) => {
      setTimeout(() => playTone(f, 'square', 0.12, 0.22), i * 45);
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

  function sfxFireworkLaunch() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    try {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      const now = audioCtx.currentTime;
      osc.frequency.setValueAtTime(260, now);
      osc.frequency.exponentialRampToValueAtTime(780, now + 0.16);
      gain.gain.setValueAtTime(0.01, now);
      gain.gain.linearRampToValueAtTime(0.14, now + 0.05);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.16);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.17);
    } catch(e) {}
  }

  function sfxSparkleBurst() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    // Acoustic sparkle cascade: crystal glockenspiel arpeggio + crisp sparkle pop
    const sparkleNotes = [1318, 1568, 1760, 2093, 2637];
    sparkleNotes.forEach((f, i) => {
      setTimeout(() => {
        playTone(f, 'sine', 0.13, 0.11);
      }, i * 26);
    });
    try {
      const bufLen = Math.floor(audioCtx.sampleRate * 0.14);
      const buf = audioCtx.createBuffer(1, bufLen, audioCtx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < bufLen; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufLen * 0.22));
      }
      const noise = audioCtx.createBufferSource();
      noise.buffer = buf;
      const flt = audioCtx.createBiquadFilter();
      flt.type = 'highpass';
      flt.frequency.value = 2400;
      const g = audioCtx.createGain();
      g.gain.setValueAtTime(0.12, audioCtx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.14);
      noise.connect(flt);
      flt.connect(g);
      g.connect(audioCtx.destination);
      noise.start();
    } catch(e) {}
  }

  function sfxHeartBurst() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    const heartMelody = [659, 830, 987, 1318];
    heartMelody.forEach((f, i) => {
      setTimeout(() => playTone(f, 'triangle', 0.15, 0.14), i * 35);
    });
  }

  function sfxLetterBurst(letter) {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    const letterFreqs = { 'A': 523, 'I': 659, 'S': 784, 'H': 987 };
    const f = letterFreqs[letter] || 880;
    playTone(f, 'square', 0.12, 0.14);
    setTimeout(() => playTone(f * 1.5, 'triangle', 0.18, 0.16), 30);
  }

  function sfxSkyBarrage() {
    initAudio();
    if (bgmMuted || !audioCtx || audioCtx.state !== 'running') return;
    const fanfare = [523, 659, 784, 1046, 1318, 1568];
    fanfare.forEach((f, i) => {
      setTimeout(() => playTone(f, 'triangle', 0.20, 0.18), i * 65);
    });
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

  // Interactive Purikura Polaroid Certificate & Sticker Decorator
  let currentPolaroidPhoto = 'portrait';
  let currentMilestoneBadge = "Queen of Frosting 👑";
  let stickersOnCard = [
    { id: 1, emoji: '👑', x: 320, y: 155, size: 46, rot: 0 },
    { id: 2, emoji: '✨', x: 135, y: 175, size: 36, rot: 0.12 },
    { id: 3, emoji: '💖', x: 505, y: 175, size: 36, rot: -0.12 }
  ];
  let selectedStickerId = null;
  let isDraggingSticker = false;
  let dragOffsetStickerX = 0;
  let dragOffsetStickerY = 0;

  function generatePolaroidCanvas(existingCanvas) {
    const cw = 640;
    const ch = 880;
    const pCanvas = existingCanvas || document.createElement('canvas');
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
    const pad = 32;
    const cardW = cw - pad * 2;
    const cardH = ch - pad * 2;
    pCtx.fillStyle = '#fdfbf7';
    pCtx.shadowColor = 'rgba(0, 0, 0, 0.75)';
    pCtx.shadowBlur = 30;
    pCtx.shadowOffsetY = 14;
    if (pCtx.roundRect) pCtx.roundRect(pad, pad, cardW, cardH, 8);
    else pCtx.rect(pad, pad, cardW, cardH);
    pCtx.fill();
    pCtx.shadowBlur = 0;
    pCtx.shadowOffsetY = 0;

    // Polaroid Card Header
    pCtx.fillStyle = '#ff007f';
    pCtx.font = 'bold 14px "Press Start 2P", sans-serif';
    pCtx.textAlign = 'center';
    pCtx.fillText("★ AISHA'S BIRTHDAY BAKE-OFF ★", cw / 2, pad + 35);

    pCtx.fillStyle = '#718096';
    pCtx.font = 'bold 8.5px "Press Start 2P", sans-serif';
    pCtx.fillText("OFFICIAL COSMIC BAKER CERTIFICATE", cw / 2, pad + 54);

    // Photo Cutout Frame
    const photoX = pad + 20;
    const photoY = pad + 68;
    const photoW = cardW - 40;
    const photoH = 480;
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
    for (let i = 0; i < 35; i++) {
      pCtx.fillStyle = pColors[i % pColors.length];
      const sx = photoX + 16 + ((i * 47) % (photoW - 32));
      const sy = photoY + 16 + ((i * 31) % (photoH - 32));
      pCtx.fillRect(sx, sy, 3, 3);
    }

    // Centered Photo Image Area
    const imgW = 270;
    const imgH = 360;
    const imgX = photoX + (photoW - imgW) / 2;
    const imgY = photoY + (photoH - imgH) / 2 + 15;

    pCtx.save();
    pCtx.strokeStyle = '#ffd700';
    pCtx.lineWidth = 4;
    pCtx.strokeRect(imgX - 2, imgY - 2, imgW + 4, imgH + 4);

    if (currentPolaroidPhoto === 'candid') {
      // Photo 2: Candid Drinking Photo
      if (aishaCandid.complete && aishaCandid.naturalWidth > 0) {
        pCtx.drawImage(aishaCandid, imgX, imgY, imgW, imgH);
      } else if (aishaPortrait.complete && aishaPortrait.naturalWidth > 0) {
        pCtx.drawImage(aishaPortrait, imgX, imgY, imgW, imgH);
      }
    } else if (currentPolaroidPhoto === 'pixel') {
      // Photo 3: Pixel-Art Aisha in Galactic Bakery
      pCtx.fillStyle = '#1a0b36';
      pCtx.fillRect(imgX, imgY, imgW, imgH);

      // Floor tiles
      pCtx.fillStyle = '#2f155c';
      for (let px = 0; px < imgW; px += 20) {
        for (let py = 0; py < imgH; py += 20) {
          if ((Math.floor(px / 20) + Math.floor(py / 20)) % 2 === 0) {
            pCtx.fillRect(imgX + px, imgY + py, 20, 20);
          }
        }
      }

      // Pixel Stars in room
      pCtx.fillStyle = '#ffd700';
      [[35, 45], [215, 55], [25, 270], [235, 250]].forEach(([sx, sy]) => {
        pCtx.fillRect(imgX + sx, imgY + sy, 5, 5);
      });

      const pxMid = imgX + imgW / 2;
      const pxY = imgY + imgH / 2 + 15;

      // Chef apron / dress
      pCtx.fillStyle = '#ff007f';
      pCtx.fillRect(pxMid - 26, pxY + 10, 52, 70);
      pCtx.fillStyle = '#ffffff';
      pCtx.fillRect(pxMid - 16, pxY + 16, 32, 55);
      pCtx.fillStyle = '#ffd700';
      pCtx.fillRect(pxMid - 5, pxY + 26, 10, 10);

      // Arms holding cake
      pCtx.fillStyle = '#fcd5b5';
      pCtx.fillRect(pxMid - 38, pxY + 22, 12, 22);
      pCtx.fillRect(pxMid + 26, pxY + 22, 12, 22);

      // 3-Tier Birthday Cake
      pCtx.fillStyle = '#00dcff';
      pCtx.fillRect(pxMid - 24, pxY + 42, 48, 15);
      pCtx.fillStyle = '#ffd700';
      pCtx.fillRect(pxMid - 17, pxY + 31, 34, 11);
      pCtx.fillStyle = '#ff4da6';
      pCtx.fillRect(pxMid - 11, pxY + 22, 22, 9);
      // Candles
      pCtx.fillStyle = '#ffea00';
      pCtx.fillRect(pxMid - 5, pxY + 14, 3, 8);
      pCtx.fillRect(pxMid + 3, pxY + 14, 3, 8);
      pCtx.fillStyle = '#ff7700';
      pCtx.fillRect(pxMid - 6, pxY + 10, 5, 4);
      pCtx.fillRect(pxMid + 2, pxY + 10, 5, 4);

      // Head
      if (aishaHead.complete && aishaHead.naturalWidth > 0) {
        const headW = 86;
        const headH = 104;
        pCtx.drawImage(aishaHead, pxMid - headW / 2, pxY - headH + 16, headW, headH);
      } else {
        pCtx.fillStyle = '#fcd5b5';
        pCtx.beginPath();
        pCtx.arc(pxMid, pxY - 32, 32, 0, Math.PI * 2);
        pCtx.fill();
      }

      // Baker Chef Hat
      pCtx.fillStyle = '#ffffff';
      pCtx.fillRect(pxMid - 28, pxY - 92, 56, 18);
      pCtx.beginPath();
      pCtx.arc(pxMid, pxY - 94, 28, Math.PI, 0);
      pCtx.fill();
      pCtx.fillStyle = '#ff007f';
      pCtx.fillRect(pxMid - 28, pxY - 78, 56, 4);
    } else {
      // Default: Official Celebration Portrait
      if (aishaPortrait.complete && aishaPortrait.naturalWidth > 0) {
        pCtx.drawImage(aishaPortrait, imgX, imgY, imgW, imgH);
      } else if (aishaHead.complete && aishaHead.naturalWidth > 0) {
        pCtx.drawImage(aishaHead, imgX, imgY, imgW, imgH);
      }
    }
    pCtx.restore();

    // Golden Birthday Tiara atop Aisha's head in photo
    const crownCenterX = imgX + imgW / 2;
    const crownTopY = imgY - 14;
    pCtx.save();
    pCtx.translate(crownCenterX, crownTopY);
    pCtx.scale(2.0, 2.0);
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

    // Render Placed Interactive Stickers
    stickersOnCard.forEach(st => {
      pCtx.save();
      pCtx.translate(st.x, st.y);
      pCtx.rotate(st.rot || 0);
      if (selectedStickerId === st.id) {
        pCtx.strokeStyle = '#00f0ff';
        pCtx.lineWidth = 2.5;
        pCtx.setLineDash([5, 5]);
        pCtx.beginPath();
        pCtx.arc(0, 0, (st.size || 42) * 0.65, 0, Math.PI * 2);
        pCtx.stroke();
        pCtx.setLineDash([]);
      }
      pCtx.font = `${st.size || 42}px sans-serif`;
      pCtx.textAlign = 'center';
      pCtx.textBaseline = 'middle';
      pCtx.fillText(st.emoji, 0, 0);
      pCtx.restore();
    });

    // Polaroid Bottom Margin
    const marginY = photoY + photoH + 24;

    // Gold Certified Master Baker Seal with Satin Ribbon
    const sealX = photoX + photoW - 65;
    const sealY = marginY + 65;
    pCtx.save();
    pCtx.fillStyle = '#ffd700';
    pCtx.shadowColor = 'rgba(218, 165, 32, 0.4)';
    pCtx.shadowBlur = 12;
    pCtx.beginPath();
    pCtx.arc(sealX, sealY, 34, 0, Math.PI * 2);
    pCtx.fill();
    pCtx.strokeStyle = '#b8860b';
    pCtx.lineWidth = 2.5;
    pCtx.stroke();

    pCtx.fillStyle = '#e6005c';
    pCtx.beginPath();
    pCtx.moveTo(sealX - 13, sealY + 26);
    pCtx.lineTo(sealX - 20, sealY + 65);
    pCtx.lineTo(sealX - 9, sealY + 56);
    pCtx.lineTo(sealX, sealY + 65);
    pCtx.lineTo(sealX - 3, sealY + 26);
    pCtx.fill();
    pCtx.beginPath();
    pCtx.moveTo(sealX + 3, sealY + 26);
    pCtx.lineTo(sealX, sealY + 65);
    pCtx.lineTo(sealX + 9, sealY + 56);
    pCtx.lineTo(sealX + 20, sealY + 65);
    pCtx.lineTo(sealX + 13, sealY + 26);
    pCtx.fill();

    pCtx.fillStyle = '#000000';
    pCtx.font = 'bold 6.5px sans-serif';
    pCtx.textAlign = 'center';
    pCtx.fillText("★ CERTIFIED ★", sealX, sealY - 7);
    pCtx.fillText("MASTER", sealX, sealY + 2);
    pCtx.fillText("BAKER 👑", sealX, sealY + 11);
    pCtx.restore();

    // Handwritten Birthday Message & Stats (Custom Wish)
    const wish = (currentPolaroidWish || "HAPPY BIRTHDAY AISHA! 🎂").trim();
    pCtx.fillStyle = '#1a202c';
    const wishFontSz = wish.length > 28 ? 13 : (wish.length > 20 ? 15 : 18);
    pCtx.font = `bold ${wishFontSz}px "Press Start 2P", cursive, sans-serif`;
    pCtx.textAlign = 'left';
    pCtx.fillText(wish, photoX, marginY + 10);

    pCtx.fillStyle = '#2b6cb0';
    pCtx.font = 'bold 11px "Press Start 2P", monospace';
    const stageTitle = (stage >= TOTAL_STAGES) ? "★ GRAND CHAMPION BAKER (ALL 30 LEVELS) ★" : `★ CERTIFIED COSMIC BAKER (STAGE ${stage}) ★`;
    pCtx.fillText(stageTitle, photoX, marginY + 42);

    pCtx.fillStyle = '#4a5568';
    pCtx.font = '10px "Press Start 2P", monospace';
    pCtx.fillText(`FINAL SCORE: ${score.toLocaleString()} PTS`, photoX, marginY + 72);

    const badgeText = currentMilestoneBadge || "Queen of Frosting 👑";
    pCtx.fillStyle = '#b83280';
    pCtx.fillText(`BADGE: ${badgeText.toUpperCase()}`, photoX, marginY + 96);

    const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    pCtx.fillStyle = '#a0aec0';
    pCtx.font = '8px "Press Start 2P", monospace';
    pCtx.fillText(`DATE: ${dateStr} • VERIFIED PURIKURA EDITION`, photoX, marginY + 126);

    return pCanvas;
  }

  function renderPolaroid() {
    const pCanvas = document.getElementById('polaroid-canvas');
    if (!pCanvas) return;
    generatePolaroidCanvas(pCanvas);
  }

  function addSticker(emoji) {
    initAudio();
    haptic(25);
    sfxCatch();
    const newSticker = {
      id: Date.now() + Math.random(),
      emoji: emoji,
      x: 320 + (Math.random() - 0.5) * 60,
      y: 330 + (Math.random() - 0.5) * 60,
      size: 42,
      rot: (Math.random() - 0.5) * 0.25
    };
    stickersOnCard.push(newSticker);
    selectedStickerId = newSticker.id;
    renderPolaroid();
  }

  function showPolaroidModal() {
    const modal = document.getElementById('polaroid-modal');
    if (modal) {
      renderPolaroid();
      modal.style.display = 'flex';
      haptic(30);
    }
  }

  function closePolaroidModal() {
    const modal = document.getElementById('polaroid-modal');
    if (modal) modal.style.display = 'none';
  }

  function shareOrSavePolaroid() {
    initAudio();
    showPolaroidModal();
  }

  async function sharePolaroid() {
    initAudio();
    haptic([30, 40]);
    const pCanvas = document.getElementById('polaroid-canvas') || generatePolaroidCanvas();
    pCanvas.toBlob(async (blob) => {
      if (!blob) return;
      const file = new File([blob], 'aisha-purikura-birthday.png', { type: 'image/png' });
      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
          await navigator.share({
            title: "Aisha's Birthday Purikura 🎂",
            text: `Happy Birthday Aisha! Conquered the Galaxy Bake-Off with ${score.toLocaleString()} points! 🎂👑`,
            files: [file]
          });
          return;
        } catch(e) {
          if (e.name !== 'AbortError') downloadPolaroid();
        }
      } else {
        downloadPolaroid();
      }
    }, 'image/png');
  }

  function downloadPolaroid() {
    initAudio();
    haptic(30);
    const pCanvas = document.getElementById('polaroid-canvas') || generatePolaroidCanvas();
    const link = document.createElement('a');
    link.download = `aisha-purikura-birthday-${Date.now()}.png`;
    link.href = pCanvas.toDataURL('image/png');
    link.click();
  }

  // Haptic feedback
  function haptic(ms) {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try { navigator.vibrate(ms); } catch(e) {}
    }
  }

  // Dynamic Viewport & Safe-Area Fitting
  let WIDTH = 720;
  let HEIGHT = 1280;
  let safeTop = 20;
  let safeBottom = 24;

  function updateSafeInsets() {
    try {
      const div = document.createElement('div');
      div.style.cssText = 'position:fixed;top:0;left:0;height:env(safe-area-inset-top, 0px);bottom:env(safe-area-inset-bottom, 0px);pointer-events:none;visibility:hidden;z-index:-999;';
      document.body.appendChild(div);
      const topPx = div.offsetHeight || 0;
      document.body.removeChild(div);
      const vh = window.innerHeight || 640;
      const scale = HEIGHT / Math.max(vh, 1);
      safeTop = Math.max(18, Math.round(topPx * scale) + 10);
      safeBottom = Math.max(20, Math.round(16 * scale));
    } catch(e) {
      safeTop = 20;
      safeBottom = 24;
    }
  }

  function handleResize() {
    const vv = window.visualViewport;
    const w = (vv ? vv.width : window.innerWidth) || 360;
    const h = (vv ? vv.height : window.innerHeight) || 640;
    const isPortrait = h >= w;
    if (isPortrait) {
      WIDTH = 720;
      const ratio = h / w;
      HEIGHT = Math.round(720 * ratio);
    } else {
      HEIGHT = 720;
      const ratio = w / h;
      WIDTH = Math.round(720 * ratio);
    }
    canvas.width = WIDTH;
    canvas.height = HEIGHT;
    updateSafeInsets();
    player.y = HEIGHT - safeBottom - 75;
    player.x = Math.max(player.w / 2, Math.min(WIDTH - player.w / 2, player.x));
  }
  window.addEventListener('resize', handleResize);
  window.addEventListener('orientationchange', () => setTimeout(handleResize, 200));
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', handleResize);
  }

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

  // Phone Tilt / Gyroscope Steering Mode (DeviceOrientationEvent)
  let tiltMode = localStorage.getItem('anti_grav_tilt') === 'true';
  let currentTiltAngle = 0;

  // Birthday Fortune Cookie Notes on Giftbox Unboxing
  const BIRTHDAY_FORTUNES = [
    "Aisha unlocked +500 Baker Karma! 💖",
    "May your year be sweeter than a 30-tier cake! 🎂",
    "Radiant Queen of the Galaxy Bakery! 👑",
    "Certified 100% Sweet & Unstoppable! ✨",
    "Wishing Aisha endless joy & laughter! 🌸",
    "Another year older, 100x more fabulous! 🍰",
    "Infinite birthday hugs & cosmic sparkles! 💫",
    "Aisha's smile outshines all stars in space! 🌟"
  ];
  let activeFortuneText = "";
  let fortuneTimer = 0;

  // Rare Birthday Shooting Star & Rainbow Fever
  let starFeverTime = 0;
  let starSpawnTimer = 18.0;

  // Custom Wish for Polaroid Certificate
  let currentPolaroidWish = "HAPPY BIRTHDAY AISHA! 🎂";

  // Furthest Stage Reached (Cake Tower Progression)
  let hiStage = parseInt(localStorage.getItem('anti_grav_histage') || '1');
  function updateHiStage(s) {
    if (s > hiStage) {
      hiStage = s;
      localStorage.setItem('anti_grav_histage', hiStage);
    }
  }

  // Retro Arcade Hall of Fame Leaderboard
  const DEFAULT_LEADERBOARD = [
    { rank: 1, name: "ASH", score: 28500, stage: 30, date: "OCT 18" },
    { rank: 2, name: "MOM", score: 19800, stage: 24, date: "OCT 18" },
    { rank: 3, name: "DAD", score: 15400, stage: 18, date: "OCT 18" },
    { rank: 4, name: "BFF", score: 12200, stage: 14, date: "OCT 18" },
    { rank: 5, name: "CAT", score: 8600,  stage: 10, date: "OCT 18" }
  ];

  let runScoreSubmitted = false;
  let pendingScore = 0;
  let pendingStage = 1;

  function getLeaderboard() {
    try {
      const stored = localStorage.getItem('anti_grav_leaderboard');
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.warn("Failed to read leaderboard:", e);
    }
    return JSON.parse(JSON.stringify(DEFAULT_LEADERBOARD));
  }

  function saveLeaderboard(list) {
    localStorage.setItem('anti_grav_leaderboard', JSON.stringify(list));
  }

  function isHighScoreEligible(s) {
    if (s <= 0) return false;
    const list = getLeaderboard();
    if (list.length < 5) return true;
    return s > list[list.length - 1].score;
  }

  function getScoreRank(s) {
    const list = getLeaderboard();
    for (let i = 0; i < list.length; i++) {
      if (s > list[i].score) return i + 1;
    }
    return Math.min(list.length + 1, 5);
  }

  function addLeaderboardEntry(name, s, st) {
    let clean = (name || "ASH").trim().toUpperCase().slice(0, 3);
    if (!clean) clean = "ASH";
    const list = getLeaderboard();
    const now = new Date();
    const months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
    const dateStr = `${months[now.getMonth()]} ${now.getDate()}`;
    const newEntry = {
      name: clean,
      score: s,
      stage: st,
      date: dateStr,
      isNew: true
    };
    list.push(newEntry);
    list.sort((a, b) => b.score - a.score);
    const top5 = list.slice(0, 5);
    top5.forEach((item, idx) => {
      item.rank = idx + 1;
    });
    saveLeaderboard(top5);
    return top5;
  }


  // Cosmic Birthday Piñata "Bonus Frenzy" (Stages 9, 19, 29)
  let pinata = {
    active: false,
    x: WIDTH / 2,
    y: 115,
    vx: 210,
    hp: 6,
    maxHp: 6,
    bobPhase: 0,
    cracked: false,
    hitFlash: 0,
    wobble: 0
  };
  let bouncingCakes = [];
  let pinataFrenzyTime = 0;
  let frenzySpawnTimer = 0;

  function initPinataForStage(stg) {
    pinata.active = true;
    pinata.cracked = false;
    pinata.hp = (stg === 29 ? 8 : (stg === 19 ? 7 : 6));
    pinata.maxHp = pinata.hp;
    pinata.x = -60;
    pinata.y = 115;
    pinata.vx = (stg === 29 ? 260 : (stg === 19 ? 230 : 200));
    pinata.hitFlash = 0;
    pinata.wobble = 0;
    pinata.bobPhase = 0;
    bouncingCakes = [];
    pinataFrenzyTime = 0;
    frenzySpawnTimer = 0;
    toastFortune("🛸 COSMIC PIÑATA INCOMING! Bounce cakes to crack! 🍬", 4.0);
  }

  function toastFortune(msg, duration = 3.6) {
    activeFortuneText = msg;
    fortuneTimer = duration;
  }

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
    if (!e.target.closest('#settings-dock-wrap')) {
      collapseSettingsDock();
    }
    if (e.target.closest('.hud-btn') || e.target.closest('.dock-btn')) return;
    if (e.target.closest('#leaderboard-modal') ||
        e.target.closest('#initials-modal') ||
        e.target.closest('#polaroid-modal') ||
        e.target.closest('#pwa-modal')) {
      return;
    }
    if (state === 'MENU') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 520);
      const boxY = HEIGHT / 2 - boxH / 2;
      if (checkpointStage > 1 && coords.y >= boxY + boxH - 110 && coords.y <= boxY + boxH - 60) {
        resumeCheckpoint();
      } else {
        startGame();
      }
      haptic(25);
      return;
    }
    if (state === 'GAME_OVER') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 520);
      const boxY = HEIGHT / 2 - boxH / 2;
      if (coords.y >= boxY + boxH - 52 && coords.y <= boxY + boxH - 24) {
        shareOrSavePolaroid();
        haptic(25);
        return;
      }
      if (checkpointStage > 1 && coords.y >= boxY + boxH - 110 && coords.y <= boxY + boxH - 60) {
        resumeCheckpoint();
      } else {
        startGame();
      }
      haptic(25);
      return;
    }
    if (state === 'WIN') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 530);
      const boxY = HEIGHT / 2 - boxH / 2;
      if (coords.y >= boxY + boxH - 56 && coords.y <= boxY + boxH - 28 && Math.abs(coords.x - WIDTH / 2) < 220) {
        shareOrSavePolaroid();
        haptic(25);
        return;
      }
      if (coords.y >= boxY + boxH - 85 && coords.y <= boxY + boxH - 58 && Math.abs(coords.x - WIDTH / 2) < 180) {
        startGame();
        haptic(25);
        return;
      }
      launchInteractiveFirework(coords.x, coords.y);
      isSkyDragging = true;
      return;
    }
    if (state === 'CANDLE_CEREMONY') {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 30, 540);
      const boxY = HEIGHT / 2 - boxH / 2;
      const cakeCenterY = HEIGHT / 2 + 75;
      if (!ceremonyAllBlown) {
        if (coords.y >= boxY + boxH - 80 && coords.y <= boxY + boxH - 35 && Math.abs(coords.x - WIDTH / 2) < 160) {
          toggleMic();
          return;
        }
        if (coords.y >= cakeCenterY - 145 && coords.y <= cakeCenterY + 70 && Math.abs(coords.x - WIDTH / 2) < 150) {
          blowCandles(coords.x, coords.y);
          return;
        }
        launchInteractiveFirework(coords.x, coords.y);
        isSkyDragging = true;
        return;
      } else {
        if (presentGachaActive && !presentGachaOpened) {
          for (let p of presents) {
            const floatY = Math.sin(globalTime * 3.5 + p.floatOffset) * 6;
            if (Math.hypot(p.x - coords.x, (p.y + floatY) - coords.y) < 55) {
              unboxPresent(p.id);
              return;
            }
          }
        }
        if (coords.y >= boxY + boxH - 60 && coords.y <= boxY + boxH - 34 && Math.abs(coords.x - WIDTH / 2) < 220) {
          shareOrSavePolaroid();
          return;
        }
        if (coords.y >= boxY + boxH - 90 && coords.y <= boxY + boxH - 62 && Math.abs(coords.x - WIDTH / 2) < 180) {
          if (stage >= TOTAL_STAGES) {
            startGame();
          } else {
            continueMilestone();
          }
          return;
        }
        launchInteractiveFirework(coords.x, coords.y);
        isSkyDragging = true;
        return;
      }
    }
    if (state === 'MILESTONE') {
      continueMilestone();
      return;
    }
    if (state === 'PAUSED') {
      const lb = document.getElementById('leaderboard-modal');
      if (lb && lb.style.display === 'flex') return;
      state = 'PLAYING';
      return;
    }
    isDragging = true;
    targetX = getCanvasCoords(e.clientX, e.clientY).x;
  }, { passive: true });

  window.addEventListener('pointermove', (e) => {
    if (isSkyDragging && (state === 'WIN' || state === 'CANDLE_CEREMONY')) {
      const coords = getCanvasCoords(e.clientX, e.clientY);
      handleSkyDrag(coords.x, coords.y);
    }
    if (!isDragging) return;
    targetX = getCanvasCoords(e.clientX, e.clientY).x;
  }, { passive: true });

  window.addEventListener('pointerup', () => { 
    isDragging = false; 
    isSkyDragging = false; 
  });
  window.addEventListener('pointercancel', () => { 
    isDragging = false; 
    isSkyDragging = false; 
  });

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

  // Touch Buttons & HUD elements
  const btnAction = { textContent: '' };
  const btnMic = document.getElementById('btn-mic');
  const btnPause = document.getElementById('pause-btn');
  const gearBtn = document.getElementById('gear-btn');
  const settingsDock = document.getElementById('settings-dock');
  const btnFS = document.getElementById('fs-btn');
  const btnMute = document.getElementById('mute-btn');
  const modalDownloadBtn = document.getElementById('modal-download-btn');
  const modalCloseBtn = document.getElementById('modal-close-btn');

  function toggleSettingsDock() {
    initAudio();
    haptic(15);
    if (!settingsDock) return;
    const isCollapsed = settingsDock.classList.contains('collapsed');
    if (isCollapsed) {
      settingsDock.classList.remove('collapsed');
      if (gearBtn) gearBtn.classList.add('open');
      playTone(660, 'sine', 0.05, 0.15);
    } else {
      collapseSettingsDock();
    }
  }

  function collapseSettingsDock() {
    if (settingsDock && !settingsDock.classList.contains('collapsed')) {
      settingsDock.classList.add('collapsed');
      if (gearBtn) gearBtn.classList.remove('open');
    }
  }

  if (gearBtn) {
    const handleGear = (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleSettingsDock();
    };
    gearBtn.addEventListener('pointerdown', handleGear);
    gearBtn.addEventListener('click', handleGear);
  }

  if (btnMute) {
    btnMute.textContent = bgmMuted ? '🔇' : '🔊';
    const handleMute = (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      setMuted(!bgmMuted);
      haptic(20);
    };
    btnMute.addEventListener('pointerdown', handleMute);
    btnMute.addEventListener('click', handleMute);
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

  // Phone Tilt / Gyroscope Steering Handler
  function handleDeviceOrientation(e) {
    if (!tiltMode) return;
    const isLandscape = window.innerWidth > window.innerHeight;
    if (isLandscape) {
      const beta = e.beta || 0;
      currentTiltAngle = Math.max(-35, Math.min(35, (window.orientation === 90 ? -beta : beta)));
    } else {
      const gamma = e.gamma || 0;
      currentTiltAngle = Math.max(-35, Math.min(35, gamma));
    }
  }

  async function toggleTiltMode() {
    initAudio();
    if (!tiltMode) {
      if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
        try {
          const perm = await DeviceOrientationEvent.requestPermission();
          if (perm !== 'granted') {
            alert("Tilt steering permission was not granted.");
            return;
          }
        } catch(err) {
          console.warn("DeviceOrientation error:", err);
        }
      }
      tiltMode = true;
      window.addEventListener('deviceorientation', handleDeviceOrientation, { passive: true });
    } else {
      tiltMode = false;
      currentTiltAngle = 0;
      window.removeEventListener('deviceorientation', handleDeviceOrientation);
    }
    localStorage.setItem('anti_grav_tilt', tiltMode);
    const tiltBtn = document.getElementById('tilt-btn');
    if (tiltBtn) tiltBtn.classList.toggle('active', tiltMode);
    haptic([25, 35]);
  }

  const btnTilt = document.getElementById('tilt-btn');
  if (btnTilt) {
    if (tiltMode) {
      btnTilt.classList.add('active');
      window.addEventListener('deviceorientation', handleDeviceOrientation, { passive: true });
    }
    btnTilt.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleTiltMode();
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

  const wishInput = document.getElementById('polaroid-wish-input');
  const wishBtn = document.getElementById('polaroid-wish-btn');
  const wishChips = document.querySelectorAll('.wish-chip');

  function updatePolaroidWish(newWish) {
    currentPolaroidWish = newWish.trim() || "HAPPY BIRTHDAY AISHA! 🎂";
    if (wishInput) wishInput.value = currentPolaroidWish;
    renderPolaroid();
    haptic(15);
  }

  // Photo Switcher Tabs
  const photoTabs = document.querySelectorAll('.photo-tab-btn');
  photoTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const pMode = btn.getAttribute('data-photo');
      if (pMode) {
        currentPolaroidPhoto = pMode;
        photoTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        sfxCatch();
        haptic(20);
        renderPolaroid();
      }
    });
  });

  // Purikura Sticker Tray Stamping
  const stickerBtns = document.querySelectorAll('.sticker-btn');
  stickerBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const emoji = btn.getAttribute('data-sticker');
      if (emoji) addSticker(emoji);
    });
  });

  const btnUndoSticker = document.getElementById('sticker-undo-btn');
  if (btnUndoSticker) {
    btnUndoSticker.addEventListener('click', () => {
      stickersOnCard.pop();
      selectedStickerId = null;
      haptic(15);
      renderPolaroid();
    });
  }

  const btnClearStickers = document.getElementById('sticker-clear-btn');
  if (btnClearStickers) {
    btnClearStickers.addEventListener('click', () => {
      stickersOnCard = [];
      selectedStickerId = null;
      haptic([20, 20]);
      renderPolaroid();
    });
  }

  // Interactive Drag & Drop of Stickers on Polaroid Canvas
  const pModalCanvas = document.getElementById('polaroid-canvas');
  if (pModalCanvas) {
    pModalCanvas.addEventListener('pointerdown', (e) => {
      const rect = pModalCanvas.getBoundingClientRect();
      const scaleX = pModalCanvas.width / rect.width;
      const scaleY = pModalCanvas.height / rect.height;
      const cx = (e.clientX - rect.left) * scaleX;
      const cy = (e.clientY - rect.top) * scaleY;

      let found = null;
      for (let i = stickersOnCard.length - 1; i >= 0; i--) {
        const st = stickersOnCard[i];
        if (Math.hypot(st.x - cx, st.y - cy) < (st.size * 0.75)) {
          found = st;
          break;
        }
      }
      if (found) {
        selectedStickerId = found.id;
        isDraggingSticker = true;
        dragOffsetStickerX = cx - found.x;
        dragOffsetStickerY = cy - found.y;
        haptic(20);
        renderPolaroid();
      } else {
        selectedStickerId = null;
        renderPolaroid();
      }
    });

    window.addEventListener('pointermove', (e) => {
      if (!isDraggingSticker || !selectedStickerId) return;
      const rect = pModalCanvas.getBoundingClientRect();
      const scaleX = pModalCanvas.width / rect.width;
      const scaleY = pModalCanvas.height / rect.height;
      const cx = (e.clientX - rect.left) * scaleX;
      const cy = (e.clientY - rect.top) * scaleY;

      const st = stickersOnCard.find(s => s.id === selectedStickerId);
      if (st) {
        st.x = Math.max(30, Math.min(pModalCanvas.width - 30, cx - dragOffsetStickerX));
        st.y = Math.max(30, Math.min(pModalCanvas.height - 30, cy - dragOffsetStickerY));
        renderPolaroid();
      }
    });

    window.addEventListener('pointerup', () => { isDraggingSticker = false; });
    window.addEventListener('pointercancel', () => { isDraggingSticker = false; });
  }

  if (wishBtn && wishInput) {
    wishBtn.addEventListener('click', () => {
      updatePolaroidWish(wishInput.value);
    });
    wishInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') updatePolaroidWish(wishInput.value);
    });
  }

  wishChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const wish = chip.getAttribute('data-wish');
      if (wish) updatePolaroidWish(wish);
    });
  });

  const modalShareBtn = document.getElementById('modal-share-btn');
  if (modalShareBtn) {
    modalShareBtn.addEventListener('click', sharePolaroid);
  }

  if (modalDownloadBtn) {
    modalDownloadBtn.addEventListener('click', downloadPolaroid);
  }

  const polaroidModal = document.getElementById('polaroid-modal');
  if (polaroidModal) {
    polaroidModal.addEventListener('click', (e) => {
      if (e.target === polaroidModal) closePolaroidModal();
    });
  }

  // Progressive Web App (PWA) Install & Service Worker Logic
  let deferredInstallPrompt = null;
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').then((reg) => {
        console.log("PWA Service Worker registered:", reg.scope);
      }).catch((err) => {
        console.warn('PWA ServiceWorker registration error:', err);
      });
    });
  }

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    updatePWAUI();
  });

  window.addEventListener('appinstalled', () => {
    deferredInstallPrompt = null;
    toastFortune("📱 Aisha's App Installed to Home Screen! 🎉");
    updatePWAUI();
  });

  const pwaBtn = document.getElementById('pwa-btn');
  const pwaModal = document.getElementById('pwa-modal');
  const pwaCloseBtn = document.getElementById('pwa-close-btn');
  const pwaActionBtn = document.getElementById('pwa-action-btn');
  const pwaPromptContainer = document.getElementById('pwa-prompt-container');

  function isStandalone() {
    return ('standalone' in window.navigator && window.navigator.standalone) ||
           window.matchMedia('(display-mode: standalone)').matches;
  }

  function isIOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  }

  function updatePWAUI() {
    if (!pwaPromptContainer) return;
    if (isStandalone()) {
      pwaPromptContainer.innerHTML = '<div style="color:#00ff88; font-size:8px; line-height:1.6; background:rgba(0,255,136,0.15); border:1px solid #00ff88; border-radius:8px; padding:10px;">★ RUNNING IN NATIVE APP MODE! ★<br><span style="color:#fff; font-size:7px;">Edge-to-edge offline gaming active!</span></div>';
      if (pwaActionBtn) pwaActionBtn.style.display = 'none';
      if (pwaBtn) pwaBtn.classList.add('installed');
    } else if (deferredInstallPrompt) {
      pwaPromptContainer.innerHTML = '<div style="color:#ffd700; font-size:8px; margin-bottom:8px;">★ Ready to install with 1 tap! ★</div>';
      if (pwaActionBtn) {
        pwaActionBtn.style.display = 'inline-block';
        pwaActionBtn.textContent = 'INSTALL NOW 📲';
      }
    } else if (isIOS()) {
      pwaPromptContainer.innerHTML = `
        <div class="pwa-ios-guide">
          <div style="font-weight:bold; color:#ffd700; margin-bottom:4px;">📲 How to Install on iPhone / iPad:</div>
          <div>1. Tap Safari\\'s <b>Share</b> button (⎋ or [↑]) at the bottom of the screen</div>
          <div>2. Scroll down &amp; tap <b>"Add to Home Screen"</b> ➕</div>
          <div>3. Tap <b>"Add"</b> in the top right corner!</div>
        </div>
      `;
      if (pwaActionBtn) pwaActionBtn.style.display = 'none';
    } else {
      pwaPromptContainer.innerHTML = `
        <div class="pwa-ios-guide" style="color:#ffd700; border-color:#ffd700;">
          <div style="font-weight:bold; margin-bottom:4px;">📲 How to Install:</div>
          <div>Tap your browser menu (<b>⋮</b>) and select <b>"Install app"</b> or <b>"Add to Home screen"</b>!</div>
        </div>
      `;
      if (pwaActionBtn) pwaActionBtn.style.display = 'none';
    }
  }

  if (pwaBtn) {
    if (isStandalone()) pwaBtn.classList.add('installed');
    pwaBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      haptic(20);
      updatePWAUI();
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        deferredInstallPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            toastFortune("📱 Aisha's App Installed to Home Screen! 🎉");
          }
          deferredInstallPrompt = null;
          updatePWAUI();
        });
      } else {
        if (pwaModal) pwaModal.style.display = 'flex';
      }
    });
  }

  if (pwaActionBtn) {
    pwaActionBtn.addEventListener('click', () => {
      initAudio();
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        deferredInstallPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            toastFortune("📱 Aisha's App Installed to Home Screen! 🎉");
          }
          deferredInstallPrompt = null;
          if (pwaModal) pwaModal.style.display = 'none';
        });
      }
    });
  }

  if (pwaCloseBtn) {
    pwaCloseBtn.addEventListener('click', () => {
      if (pwaModal) pwaModal.style.display = 'none';
    });
  }
  if (pwaModal) {
    pwaModal.addEventListener('click', (e) => {
      if (e.target === pwaModal) pwaModal.style.display = 'none';
    });
  }

  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ─── RETRO ARCADE INITIALS ENTRY UI LOGIC ─────────────────────────────
  const initialsModal = document.getElementById('initials-modal');
  const initialsRankTitle = document.getElementById('initials-rank-title');
  const initialsScoreText = document.getElementById('initials-score-text');
  const initialsInput = document.getElementById('initials-input');
  const initialsSubmitBtn = document.getElementById('initials-submit-btn');
  const initialsSkipBtn = document.getElementById('initials-skip-btn');
  const slot0 = document.getElementById('slot-0');
  const slot1 = document.getElementById('slot-1');
  const slot2 = document.getElementById('slot-2');
  let currentInitials = "ASH";

  function promptInitials(s, st) {
    pendingScore = s;
    pendingStage = st;
    const rank = getScoreRank(s);
    if (initialsRankTitle) initialsRankTitle.textContent = `TOP 5 BAKER: RANK #${rank}!`;
    if (initialsScoreText) initialsScoreText.textContent = `${s.toLocaleString()} PTS (STAGE ${st})`;
    currentInitials = "ASH";
    updateInitialsSlots();
    if (initialsModal) initialsModal.style.display = 'flex';
    if (initialsInput) {
      initialsInput.value = currentInitials;
      try { initialsInput.focus(); } catch(e){}
    }
    playTone(587, 'triangle', 0.1, 0.2);
    setTimeout(() => playTone(880, 'triangle', 0.2, 0.25), 100);
  }

  function closeInitialsModal() {
    if (initialsModal) initialsModal.style.display = 'none';
  }

  function updateInitialsSlots() {
    const chars = currentInitials.padEnd(3, ' ').split('');
    if (slot0) slot0.textContent = chars[0] !== ' ' ? chars[0] : '_';
    if (slot1) slot1.textContent = chars[1] !== ' ' ? chars[1] : '_';
    if (slot2) slot2.textContent = chars[2] !== ' ' ? chars[2] : '_';

    const activeIdx = Math.min(currentInitials.length, 2);
    [slot0, slot1, slot2].forEach((el, idx) => {
      if (el) el.classList.toggle('active', idx === activeIdx);
    });
  }

  function appendInitialChar(ch) {
    initAudio();
    haptic(15);
    playTone(700, 'square', 0.04, 0.1);
    if (currentInitials.length < 3) {
      currentInitials += ch.toUpperCase();
      updateInitialsSlots();
    }
  }

  function backspaceInitial() {
    initAudio();
    haptic(15);
    playTone(400, 'triangle', 0.05, 0.1);
    if (currentInitials.length > 0) {
      currentInitials = currentInitials.slice(0, -1);
      updateInitialsSlots();
    }
  }

  function submitPlayerInitials() {
    initAudio();
    haptic([30, 40, 60]);
    let name = currentInitials.trim().toUpperCase() || 'ASH';
    addLeaderboardEntry(name, pendingScore, pendingStage);
    runScoreSubmitted = true;
    closeInitialsModal();
    playTone(523, 'sine', 0.1, 0.2);
    setTimeout(() => playTone(659, 'sine', 0.1, 0.2), 90);
    setTimeout(() => playTone(784, 'sine', 0.15, 0.25), 180);
    setTimeout(() => playTone(1046, 'sine', 0.3, 0.3), 270);
    openLeaderboardModal(true);
  }

  if (initialsSubmitBtn) {
    initialsSubmitBtn.addEventListener('click', (e) => {
      e.preventDefault();
      submitPlayerInitials();
    });
  }

  const initialsCloseX = document.getElementById('initials-close-x');
  function skipPlayerInitials() {
    runScoreSubmitted = true;
    closeInitialsModal();
    openLeaderboardModal(false);
  }
  if (initialsSkipBtn) {
    initialsSkipBtn.addEventListener('click', (e) => {
      e.preventDefault();
      skipPlayerInitials();
    });
  }
  if (initialsCloseX) {
    initialsCloseX.addEventListener('click', (e) => {
      e.preventDefault();
      skipPlayerInitials();
    });
  }

  // Quick initial chips
  document.querySelectorAll('.quick-chip').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const inits = btn.getAttribute('data-initials') || 'ASH';
      currentInitials = inits.slice(0, 3).toUpperCase();
      updateInitialsSlots();
      haptic(20);
      playTone(800, 'sine', 0.05, 0.15);
    });
  });

  // Arcade keypad buttons
  document.querySelectorAll('.arcade-key').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (btn.id === 'key-backspace') {
        backspaceInitial();
      } else {
        const char = btn.getAttribute('data-char');
        if (char) appendInitialChar(char);
      }
    });
  });

  // Native input sync
  if (initialsInput) {
    initialsInput.addEventListener('input', () => {
      currentInitials = initialsInput.value.replace(/[^a-zA-Z0-9★]/g, '').toUpperCase().slice(0, 3);
      updateInitialsSlots();
    });
    initialsInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitPlayerInitials();
      }
    });
  }

  // ─── RETRO ARCADE HALL OF FAME LEADERBOARD (MINI WINDOW) ────────────────
  const leaderboardModal = document.getElementById('leaderboard-modal');
  const leaderboardTable = document.getElementById('leaderboard-table');
  const lbCurrentStat = document.getElementById('leaderboard-current-stat');
  const lbShareBtn = document.getElementById('lb-share-btn');
  const lbResetBtn = document.getElementById('lb-reset-btn');
  const lbCloseBtn = document.getElementById('lb-close-btn');
  const lbCloseX = document.getElementById('lb-close-x');
  const leaderboardBtn = document.getElementById('leaderboard-btn');

  let wasPlayingBeforeLeaderboard = false;

  function openLeaderboardModal(highlightNew = false) {
    initAudio();
    haptic(20);
    collapseSettingsDock();

    // Auto-pause if actively playing
    if (state === 'PLAYING') {
      wasPlayingBeforeLeaderboard = true;
      state = 'PAUSED';
      syncUIState();
    }

    renderLeaderboard(highlightNew);
    if (leaderboardModal) leaderboardModal.style.display = 'flex';
  }

  function closeLeaderboardModal() {
    initAudio();
    haptic(15);
    if (leaderboardModal) leaderboardModal.style.display = 'none';
    collapseSettingsDock();

    // Auto-resume gameplay if it was paused when opening
    if (wasPlayingBeforeLeaderboard) {
      wasPlayingBeforeLeaderboard = false;
      if (state === 'PAUSED') {
        state = 'PLAYING';
        lastTime = performance.now();
        syncUIState();
      }
    }
  }

  function renderLeaderboard(highlightNew = false) {
    const list = getLeaderboard();
    if (lbCurrentStat) {
      lbCurrentStat.textContent = `LATEST RUN: ${score.toLocaleString()} PTS (STAGE ${stage})`;
    }
    if (!leaderboardTable) return;
    leaderboardTable.innerHTML = '';

    list.forEach(entry => {
      const row = document.createElement('div');
      row.className = `lb-row rank-${entry.rank}` + (highlightNew && entry.isNew ? ' new-entry-glow' : '');
      const trophy = entry.rank === 1 ? '🥇' : (entry.rank === 2 ? '🥈' : (entry.rank === 3 ? '🥉' : `#${entry.rank}`));
      const stageText = `LVL ${entry.stage || 1}`;

      row.innerHTML = `
        <div class="lb-left">
          <div class="lb-trophy">${trophy}</div>
          <div>
            <div class="lb-name">${escapeHTML(entry.name)}</div>
            <div style="font-size: 5.5px; color: #859bb8; margin-top: 1px;">${entry.date || 'OCT 18'}</div>
          </div>
        </div>
        <div class="lb-right">
          <div class="lb-score">${(entry.score || 0).toLocaleString()} <span style="font-size:6.5px; color:#ff6ebe;">PTS</span></div>
          <div class="lb-stage-tag">${stageText}</div>
        </div>
      `;
      leaderboardTable.appendChild(row);
      delete entry.isNew;
    });
  }

  async function shareLeaderboard() {
    initAudio();
    haptic(20);
    const list = getLeaderboard();
    let text = `🏆 AISHA'S BIRTHDAY BAKE-OFF: HALL OF FAME 🏆
`;
    list.forEach(item => {
      const medal = item.rank === 1 ? "🥇" : (item.rank === 2 ? "🥈" : (item.rank === 3 ? "🥉" : `[#${item.rank}]`));
      text += `${medal} ${item.name} — ${item.score.toLocaleString()} pts (Lvl ${item.stage})
`;
    });
    text += `
Can you beat Aisha and friends' cosmic high scores? 🎂✨
https://aishababu.vercel.app`;

    if (navigator.share) {
      try {
        await navigator.share({
          title: "Aisha's Bake-Off Hall of Fame 🏆",
          text: text,
          url: "https://aishababu.vercel.app"
        });
        return;
      } catch (err) {
        if (err.name !== 'AbortError') console.warn(err);
      }
    }
    try {
      await navigator.clipboard.writeText(text);
      if (lbShareBtn) {
        const orig = lbShareBtn.textContent;
        lbShareBtn.textContent = "COPIED! ✨";
        setTimeout(() => { lbShareBtn.textContent = orig; }, 1800);
      }
      toastFortune("🏆 Leaderboard copied to clipboard!");
    } catch (e) {
      prompt("Copy Hall of Fame:", text);
    }
  }

  function resetLeaderboard() {
    initAudio();
    haptic(30);
    if (confirm("Reset Hall of Fame scores back to default family records?")) {
      saveLeaderboard(DEFAULT_LEADERBOARD);
      renderLeaderboard(false);
      playTone(440, 'triangle', 0.1, 0.2);
    }
  }

  const leaderboardWrap = document.getElementById('leaderboard-wrap');
  if (leaderboardWrap) {
    leaderboardWrap.addEventListener('pointerdown', (e) => e.stopPropagation());
    leaderboardWrap.addEventListener('click', (e) => e.stopPropagation());
  }

  if (lbShareBtn) {
    lbShareBtn.addEventListener('click', shareLeaderboard);
  }
  if (lbResetBtn) {
    lbResetBtn.addEventListener('click', resetLeaderboard);
  }
  if (lbCloseBtn) {
    const handleCloseBtn = (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeLeaderboardModal();
    };
    lbCloseBtn.addEventListener('pointerdown', handleCloseBtn);
    lbCloseBtn.addEventListener('click', handleCloseBtn);
  }
  if (lbCloseX) {
    const handleCloseX = (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeLeaderboardModal();
    };
    lbCloseX.addEventListener('pointerdown', handleCloseX);
    lbCloseX.addEventListener('click', handleCloseX);
  }
  if (leaderboardBtn) {
    const handleOpenLeaderboard = (e) => {
      e.preventDefault();
      e.stopPropagation();
      openLeaderboardModal();
    };
    leaderboardBtn.addEventListener('pointerdown', handleOpenLeaderboard);
    leaderboardBtn.addEventListener('click', handleOpenLeaderboard);
  }
  if (leaderboardModal) {
    leaderboardModal.addEventListener('click', (e) => {
      if (e.target === leaderboardModal) closeLeaderboardModal();
    });
  }
  function syncUIState() {
    checkpointStage = parseInt(localStorage.getItem('anti_grav_checkpoint') || '0');
    checkpointScore = parseInt(localStorage.getItem('anti_grav_checkpoint_score') || '0');

    if (btnMic) {
      if (state === 'CANDLE_CEREMONY' && !ceremonyAllBlown) {
        btnMic.style.display = 'flex';
        btnMic.classList.toggle('active', micEnabled);
      } else {
        btnMic.style.display = 'none';
      }
    }
  }

  if (btnMic) {
    btnMic.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      initAudio();
      toggleMic();
      haptic(20);
    });
  }

  btnPause.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    collapseSettingsDock();
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

  function drawStarShape(ctx, cx, cy, spikes=5, outerRadius=12, innerRadius=5.5) {
    let rot = Math.PI / 2 * 3;
    let x = cx;
    let y = cy;
    const step = Math.PI / spikes;
    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);
    for (let i = 0; i < spikes; i++) {
      x = cx + Math.cos(rot) * outerRadius;
      y = cy + Math.sin(rot) * outerRadius;
      ctx.lineTo(x, y);
      rot += step;
      x = cx + Math.cos(rot) * innerRadius;
      y = cy + Math.sin(rot) * innerRadius;
      ctx.lineTo(x, y);
      rot += step;
    }
    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
  }

  function drawHeartShape(ctx, cx, cy, size=12) {
    ctx.beginPath();
    const topCurveHeight = size * 0.35;
    const topY = cy - size * 0.35;
    ctx.moveTo(cx, topY + topCurveHeight);
    ctx.bezierCurveTo(cx, topY, cx - size / 2, topY, cx - size / 2, topY + topCurveHeight);
    ctx.bezierCurveTo(cx - size / 2, topY + (size + topCurveHeight) / 2, cx, topY + size, cx, topY + size);
    ctx.bezierCurveTo(cx, topY + size, cx + size / 2, topY + (size + topCurveHeight) / 2, cx + size / 2, topY + topCurveHeight);
    ctx.bezierCurveTo(cx + size / 2, topY, cx, topY, cx, topY + topCurveHeight);
    ctx.closePath();
  }

  const LETTER_MATRICES = {
    'A': [
      "  XXX  ",
      " X   X ",
      " X   X ",
      " XXXXX ",
      " X   X ",
      " X   X ",
      " X   X "
    ],
    'I': [
      " XXXXX ",
      "   X   ",
      "   X   ",
      "   X   ",
      "   X   ",
      "   X   ",
      " XXXXX "
    ],
    'S': [
      "  XXXX ",
      " X     ",
      " X     ",
      "  XXX  ",
      "     X ",
      "     X ",
      " XXXX  "
    ],
    'H': [
      " X   X ",
      " X   X ",
      " X   X ",
      " XXXXX ",
      " X   X ",
      " X   X ",
      " X   X "
    ]
  };

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

  function addHeartFireworks(x, y, color) {
    sfxFireworkLaunch();
    setTimeout(() => {
      sfxHeartBurst();
      haptic([30, 20, 45]);

      const heartCols = ['#ff007f', '#ff4da6', '#ff6ebe', '#ff85c0', '#ffffff', '#ff1493'];
      const count = 42;
      for (let i = 0; i < count; i++) {
        const t = (i / count) * Math.PI * 2;
        const hx = 16 * Math.pow(Math.sin(t), 3);
        const hy = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
        const spd = 9.8 + (Math.random() - 0.5) * 0.8;
        const col = color || heartCols[i % heartCols.length];
        particles.push({
          x: x,
          y: y,
          vx: hx * spd,
          vy: hy * spd,
          life: 1.3,
          maxLife: 1.3,
          color: col,
          size: 3.5,
          shape: 'heart',
          drag: 0.65,
          gravity: 28,
          glow: 14,
          trail: true
        });
      }

      // Inner glitter love embers
      for (let k = 0; k < 16; k++) {
        const t = Math.random() * Math.PI * 2;
        const hx = 16 * Math.pow(Math.sin(t), 3);
        const hy = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
        const scale = 0.25 + Math.random() * 0.55;
        const spd = 9.8 * scale;
        particles.push({
          x: x,
          y: y,
          vx: hx * spd,
          vy: hy * spd,
          life: 1.45,
          maxLife: 1.45,
          color: ['#ffe082', '#ffffff', '#ff6ebe'][k % 3],
          size: 2.5,
          shape: 'sparkle',
          drag: 0.85,
          gravity: 20,
          glow: 10
        });
      }

      addScorePopup(x, y - 25, "💖", '#ff4da6');
    }, 60);
  }

  function addStarFireworks(x, y) {
    sfxFireworkLaunch();
    setTimeout(() => {
      sfxSparkleBurst();
      haptic([25, 20, 25, 20]);

      const colors = ['#ffd700', '#fff4a3', '#ffffff', '#ffee55', '#ffb700'];
      const vertices = [];
      for (let k = 0; k < 10; k++) {
        const ang = -Math.PI / 2 + (k * Math.PI / 5);
        const rad = (k % 2 === 0) ? 175 : 75;
        vertices.push({ vx: Math.cos(ang) * rad, vy: Math.sin(ang) * rad });
      }

      // Edge particles forming the star outline
      for (let k = 0; k < 10; k++) {
        const v1 = vertices[k];
        const v2 = vertices[(k + 1) % 10];
        for (let s = 0; s < 4; s++) {
          const frac = s / 4;
          const vx = v1.vx * (1 - frac) + v2.vx * frac;
          const vy = v1.vy * (1 - frac) + v2.vy * frac;
          const col = colors[(k * 4 + s) % colors.length];
          particles.push({
            x: x,
            y: y,
            vx: vx * (0.95 + Math.random() * 0.1),
            vy: vy * (0.95 + Math.random() * 0.1),
            life: 1.3,
            maxLife: 1.3,
            color: col,
            size: 3.5,
            shape: 'star',
            drag: 0.6,
            gravity: 30,
            glow: 14,
            trail: true
          });
        }
      }

      // 5 Shooting Tips
      for (let k = 0; k < 5; k++) {
        const ang = -Math.PI / 2 + (k * 2 * Math.PI / 5);
        [1.25, 1.45].forEach(mult => {
          particles.push({
            x: x,
            y: y,
            vx: Math.cos(ang) * 175 * mult,
            vy: Math.sin(ang) * 175 * mult,
            life: 1.4,
            maxLife: 1.4,
            color: '#ffffff',
            size: 4,
            shape: 'sparkle',
            drag: 0.7,
            gravity: 35,
            glow: 18,
            trail: true
          });
        });
      }

      addScorePopup(x, y - 25, "⭐", '#ffd700');
    }, 60);
  }

  function addLetterFireworks(x, y, letter='A', color='#ffd700') {
    sfxFireworkLaunch();
    setTimeout(() => {
      sfxLetterBurst(letter);
      haptic(45);

      const matrix = LETTER_MATRICES[letter] || LETTER_MATRICES['A'];
      const spacing = 11;
      const palette = [color, '#ffffff', '#ff6ebe', '#00dcff'];

      // Generate letter constellation particles
      matrix.forEach((rowStr, r) => {
        for (let c = 0; c < rowStr.length; c++) {
          if (rowStr[c] === 'X') {
            const ox = (c - 3) * spacing;
            const oy = (r - 3) * spacing;
            const spd = 3.6 + Math.random() * 0.4;
            const pCol = palette[Math.floor(Math.random() * palette.length)];
            particles.push({
              x: x,
              y: y,
              vx: ox * spd + (Math.random() - 0.5) * 8,
              vy: oy * spd + (Math.random() - 0.5) * 8,
              life: 1.45,
              maxLife: 1.45,
              color: pCol,
              size: 3.5,
              shape: 'sparkle',
              drag: 2.1,
              gravity: 12,
              glow: 14,
              trail: true
            });
          }
        }
      });

      // Central glowing letter text
      particles.push({
        x: x,
        y: y,
        vx: 0,
        vy: -15,
        life: 1.5,
        maxLife: 1.5,
        text: letter,
        color: color,
        fontSize: 28,
        isText: true,
        glow: 20
      });

      // Embers bursting around letter
      for (let k = 0; k < 14; k++) {
        const ang = Math.random() * Math.PI * 2;
        const spd = 60 + Math.random() * 120;
        particles.push({
          x: x,
          y: y,
          vx: Math.cos(ang) * spd,
          vy: Math.sin(ang) * spd,
          life: 0.9,
          maxLife: 0.9,
          color: palette[k % palette.length],
          size: 2.5,
          shape: 'star',
          drag: 1.0,
          gravity: 25,
          glow: 8
        });
      }
    }, 60);
  }

  function addAISHAWordFireworks(targetY) {
    const letters = ['A', 'I', 'S', 'H', 'A'];
    const colors = ['#ff007f', '#00dcff', '#ffd700', '#76ff03', '#ff6ebe'];
    const y = targetY || (HEIGHT * 0.28);
    const xPositions = [
      WIDTH * 0.16,
      WIDTH * 0.33,
      WIDTH * 0.50,
      WIDTH * 0.67,
      WIDTH * 0.84
    ];

    sfxSkyBarrage();
    letters.forEach((lt, idx) => {
      setTimeout(() => {
        addLetterFireworks(xPositions[idx], y, lt, colors[idx]);
      }, idx * 150);
    });

    setTimeout(() => {
      addScorePopup(WIDTH / 2, y - 65, "✨ HAPPY BIRTHDAY AISHA! ✨", '#ffd700');
      addHeartFireworks(WIDTH * 0.14, y + 40);
      addHeartFireworks(WIDTH * 0.86, y + 40);
      haptic([50, 40, 50, 40, 100]);
    }, letters.length * 150 + 200);
  }

  let fireworkShapeCycle = 0;
  const AISHA_SEQUENCE = ['A', 'I', 'S', 'H', 'A'];
  let aishaSeqIdx = 0;

  function launchInteractiveFirework(x, y) {
    // If touched near top of the sky, trigger the majestic 5-burst AISHA barrage!
    if (y < HEIGHT * 0.18) {
      addAISHAWordFireworks(y + 60);
      return;
    }

    const mode = fireworkShapeCycle % 3;
    fireworkShapeCycle++;

    if (mode === 0) {
      addHeartFireworks(x, y);
    } else if (mode === 1) {
      addStarFireworks(x, y);
    } else {
      const letter = AISHA_SEQUENCE[aishaSeqIdx % AISHA_SEQUENCE.length];
      aishaSeqIdx++;
      addLetterFireworks(x, y, letter, ['#ffd700', '#00dcff', '#ff007f', '#76ff03', '#ff6ebe'][aishaSeqIdx % 5]);
      if (aishaSeqIdx > 0 && (aishaSeqIdx % AISHA_SEQUENCE.length === 0)) {
        setTimeout(() => {
          addAISHAWordFireworks(Math.min(y, HEIGHT * 0.32));
        }, 400);
      }
    }
  }

  let isSkyDragging = false;
  let lastDragSparkleTime = 0;
  let lastDragSfxTime = 0;

  function handleSkyDrag(x, y) {
    const now = performance.now();
    if (now - lastDragSparkleTime > 40) {
      lastDragSparkleTime = now;
      const dragCols = ['#ffd700', '#ff6ebe', '#00dcff', '#ffffff', '#ff007f'];
      for (let k = 0; k < 3; k++) {
        particles.push({
          x: x + (Math.random() - 0.5) * 22,
          y: y + (Math.random() - 0.5) * 22,
          vx: (Math.random() - 0.5) * 60,
          vy: -30 - Math.random() * 45,
          life: 0.7,
          maxLife: 0.7,
          color: dragCols[Math.floor(Math.random() * dragCols.length)],
          size: 2.8,
          shape: Math.random() < 0.5 ? 'star' : 'heart',
          drag: 1.1,
          gravity: 25,
          glow: 10
        });
      }
      if (now - lastDragSfxTime > 140) {
        lastDragSfxTime = now;
        playTone(1480 + Math.random() * 400, 'sine', 0.08, 0.06);
        haptic(10);
      }
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

  // Mystery Birthday Present Unboxing (Milestone Bonus Gacha)
  let presentGachaActive = false;
  let presentGachaOpened = false;
  let presents = [];
  let gachaWonBadge = null;
  let gachaWonPerk = null;
  let activeRoundPerk = null;

  const GACHA_REWARDS = [
    {
      badge: "Queen of Frosting 👑",
      perkName: "🧲 Starting Golden Magnet (8s)!",
      perkType: "MAGNET",
      perkVal: 8,
      desc: "Attracts all falling treats directly to your basket!"
    },
    {
      badge: "Galaxy Flame Master 🔥",
      perkName: "💖 +500 Baker Karma Bonus!",
      perkType: "KARMA",
      perkVal: 500,
      desc: "+500 bonus points added directly to your score!"
    },
    {
      badge: "Candle Whisperer 🕯️",
      perkName: "🛡️ Starting Sweet Shield!",
      perkType: "SHIELD",
      perkVal: 1,
      desc: "Immunity against the next anvil or spoiled hazard!"
    },
    {
      badge: "Berry Royal Alchemist 🍓",
      perkName: "⏱️ Chronos Time Warp (+15s)!",
      perkType: "TIME",
      perkVal: 15,
      desc: "+15 extra seconds on the bakery clock next stage!"
    },
    {
      badge: "Star Confectioner ⭐",
      perkName: "🍬 Sugar Rush Frenzy (6 Treats)!",
      perkType: "SUGAR_RUSH",
      perkVal: 6,
      desc: "Triple combo multiplier for the first 6 treats!"
    },
    {
      badge: "Cosmic Baker Supreme 🎂",
      perkName: "🌟 Rainbow Star-Fever (5s)!",
      perkType: "STAR_FEVER",
      perkVal: 5,
      desc: "Invincible rainbow runner and hazards turn to cupcakes!"
    }
  ];

  function initMilestoneGacha() {
    presentGachaActive = true;
    presentGachaOpened = false;
    gachaWonBadge = null;
    gachaWonPerk = null;

    const boxH = Math.min(HEIGHT - safeTop - safeBottom - 30, 540);
    const boxY = HEIGHT / 2 - boxH / 2;
    const offsets = [-140, 0, 140];
    const boxColors = [
      { box: '#ff007f', ribbon: '#ffd700', lid: '#ff4da6' },
      { box: '#ffd700', ribbon: '#ff007f', lid: '#ffea00' },
      { box: '#00dcff', ribbon: '#ffffff', lid: '#70e000' }
    ];

    presents = offsets.map((ox, idx) => ({
      id: idx,
      x: WIDTH / 2 + ox,
      y: boxY + 280,
      w: 76,
      h: 76,
      colors: boxColors[idx],
      floatOffset: idx * 1.6,
      opened: false
    }));

    btnAction.textContent = 'PICK GIFT 🎁';
  }

  function unboxPresent(idx) {
    if (presentGachaOpened) return;
    presentGachaOpened = true;
    const p = presents[idx] || presents[1];
    p.opened = true;

    const reward = GACHA_REWARDS[Math.floor(Math.random() * GACHA_REWARDS.length)];
    gachaWonBadge = reward.badge;
    gachaWonPerk = reward;
    currentMilestoneBadge = reward.badge;
    activeRoundPerk = reward;

    if (reward.perkType === 'KARMA') {
      score += reward.perkVal;
      if (score > hiScore) {
        hiScore = score;
        localStorage.setItem('anti_grav_hiscore', hiScore);
      }
    }

    sfxPowerup();
    setTimeout(() => sfxSparkleBurst(), 160);
    haptic([40, 30, 60, 40, 120]);

    for (let k = 0; k < 50; k++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = 120 + Math.random() * 260;
      particles.push({
        x: p.x,
        y: p.y,
        vx: Math.cos(ang) * spd,
        vy: Math.sin(ang) * spd - 60,
        life: 1.4,
        maxLife: 1.4,
        color: ['#ffd700', '#ff007f', '#00dcff', '#76ff03', '#ffffff'][k % 5],
        size: 3 + Math.random() * 3,
        shape: Math.random() < 0.5 ? 'star' : 'heart',
        drag: 0.8,
        gravity: 45,
        glow: 12
      });
    }

    addScorePopup(p.x, p.y - 45, "🎁 " + reward.badge, COLORS.GOLD);

    btnAction.textContent = (stage < TOTAL_STAGES) ? ('STAGE ' + (stage + 1) + ' ▶') : 'PLAY AGAIN ★';
    syncUIState();
  }

  function initCandleCeremony() {
    ceremonyAllBlown = false;
    ceremonySmokeParticles = [];
    ceremonyCandles = [];
    presentGachaActive = false;
    presentGachaOpened = false;

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
      if (presentGachaActive && !presentGachaOpened) {
        unboxPresent(1);
        return;
      }
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
        initMilestoneGacha();
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
        btnAction.textContent = 'PICK GIFT 🎁';
        syncUIState();
      }
    }
  }

  function activatePowerup(type) {
    // Unbox Birthday Fortune Cookie Message
    activeFortuneText = BIRTHDAY_FORTUNES[Math.floor(Math.random() * BIRTHDAY_FORTUNES.length)];
    fortuneTimer = 3.6;
    for (let k = 0; k < 12; k++) {
      particles.push({
        x: player.x + (Math.random() - 0.5) * 60,
        y: player.y - 120,
        vx: (Math.random() - 0.5) * 180,
        vy: -60 - Math.random() * 80,
        size: 3 + Math.random() * 3,
        color: ['#ffd700', '#ff6ebe', '#00dcff', '#37be46'][k % 4],
        life: 0.8,
        maxLife: 0.8
      });
    }

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
    runScoreSubmitted = false;
    updateHiStage(stage);
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    shakeTime = 0;
    comboStreak = 0;
    magnetTime = 0;
    shieldActive = false;
    slowmoTime = 0;
    sugarRushCount = 0;
    starFeverTime = 0;
    starSpawnTimer = 18.0;
    fortuneTimer = 0;
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
    collapseSettingsDock();
    btnAction.textContent = 'PAUSE';
    if (stage === 9 || stage === 19 || stage === 29) {
      initPinataForStage(stage);
    } else {
      pinata.active = false;
      bouncingCakes = [];
      pinataFrenzyTime = 0;
    }
    syncUIState();
  }

  function resumeCheckpoint() {
    const cpStage = parseInt(localStorage.getItem('anti_grav_checkpoint') || '1');
    const cpScore = parseInt(localStorage.getItem('anti_grav_checkpoint_score') || '0');
    runScoreSubmitted = false;
    updateHiStage(cpStage);
    startGame(cpStage, cpScore);
  }

  function continueMilestone() {
    stopMic();
    stopHappyBirthdaySong();
    collapseSettingsDock();
    stage++;
    updateHiStage(stage);
    itemsCaughtStage = 0;
    timeLeft = STAGE_DURATION;
    items = [];
    hazardWarnings = [];
    comboStreak = 0;
    ceremonyCandles = [];
    ceremonyAllBlown = false;
    ceremonySmokeParticles = [];
    presentGachaActive = false;
    presentGachaOpened = false;

    // Apply won perk from Gacha!
    if (activeRoundPerk) {
      if (activeRoundPerk.perkType === 'MAGNET') {
        magnetTime = activeRoundPerk.perkVal;
        addScorePopup(player.x, player.y - 70, "🧲 PERK: MAGNET ACTIVE!", COLORS.GOLD);
      } else if (activeRoundPerk.perkType === 'SHIELD') {
        shieldActive = true;
        addScorePopup(player.x, player.y - 70, "🛡️ PERK: SHIELD ACTIVE!", COLORS.CYAN);
      } else if (activeRoundPerk.perkType === 'TIME') {
        timeLeft += activeRoundPerk.perkVal;
        addScorePopup(player.x, player.y - 70, `⏱️ PERK: +${activeRoundPerk.perkVal}s TIME!`, COLORS.CYAN);
      } else if (activeRoundPerk.perkType === 'SUGAR_RUSH') {
        sugarRushCount = activeRoundPerk.perkVal;
        addScorePopup(player.x, player.y - 70, "🍬 PERK: SUGAR RUSH!", COLORS.GOLD);
      } else if (activeRoundPerk.perkType === 'STAR_FEVER') {
        starFeverTime = activeRoundPerk.perkVal;
        sfxStarFever();
        addScorePopup(player.x, player.y - 70, "⭐ PERK: STAR FEVER!", COLORS.GOLD);
      }
      activeRoundPerk = null;
    }

    state = 'PLAYING';
    btnAction.textContent = 'PAUSE';
    if (stage === 9 || stage === 19 || stage === 29) {
      initPinataForStage(stage);
    } else {
      pinata.active = false;
      bouncingCakes = [];
      pinataFrenzyTime = 0;
    }
    syncUIState();
    sfxCatch();
    haptic(30);
  }

  function nextStage() {
    stopMic();
    stopHappyBirthdaySong();
    collapseSettingsDock();
    stage++;
    updateHiStage(stage);
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
      if (!runScoreSubmitted) {
        runScoreSubmitted = true;
        if (isHighScoreEligible(score)) {
          setTimeout(() => promptInitials(score, 30), 600);
        } else {
          setTimeout(() => openLeaderboardModal(false), 700);
        }
      }
    } else {
      itemsCaughtStage = 0;
      timeLeft = STAGE_DURATION;
      items = [];
      hazardWarnings = [];
      state = 'PLAYING';
      btnAction.textContent = 'PAUSE';
      if (stage === 9 || stage === 19 || stage === 29) {
        initPinataForStage(stage);
      } else {
        pinata.active = false;
        bouncingCakes = [];
        pinataFrenzyTime = 0;
      }
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
    if (!runScoreSubmitted) {
      runScoreSubmitted = true;
      if (isHighScoreEligible(score)) {
        setTimeout(() => promptInitials(score, stage), 450);
      } else {
        setTimeout(() => openLeaderboardModal(false), 500);
      }
    }
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

  function drawShootingStar(ctx, x, y, rot, time) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);

    // Pulsating rainbow chromatic aura
    const rColors = ['#ff0077', '#00dcff', '#ffd700', '#70e000', '#bd00ff'];
    const auraCol = rColors[Math.floor(time * 10) % rColors.length];
    ctx.shadowColor = auraCol;
    ctx.shadowBlur = 24;

    // Outer glow rays
    ctx.strokeStyle = auraCol;
    ctx.lineWidth = 2.5;
    for (let r = 0; r < 4; r++) {
      const a = (r / 4) * Math.PI;
      ctx.beginPath();
      ctx.moveTo(Math.cos(a) * -22, Math.sin(a) * -22);
      ctx.lineTo(Math.cos(a) * 22, Math.sin(a) * 22);
      ctx.stroke();
    }

    // 5-point golden shooting star
    ctx.fillStyle = '#ffd700';
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {
      const a1 = (i * 4 * Math.PI) / 5 - Math.PI / 2;
      const rx = Math.cos(a1) * 16;
      const ry = Math.sin(a1) * 16;
      if (i === 0) ctx.moveTo(rx, ry);
      else ctx.lineTo(rx, ry);
    }
    ctx.closePath();
    ctx.fill();

    // Center sparkling diamond jewel
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(0, 0, 4.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function drawCupcake(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);
    ctx.scale(1.4, 1.4);

    // Golden halo
    ctx.shadowColor = '#ffd700';
    ctx.shadowBlur = 14;

    // Gold pleated cupcake cup
    ctx.fillStyle = '#e5a500';
    ctx.beginPath();
    ctx.moveTo(-11, 2);
    ctx.lineTo(11, 2);
    ctx.lineTo(8, 14);
    ctx.lineTo(-8, 14);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#fff3a0';
    ctx.lineWidth = 1;
    [-4, 0, 4].forEach(px => {
      ctx.beginPath(); ctx.moveTo(px, 3); ctx.lineTo(px * 0.8, 13); ctx.stroke();
    });

    // Swirled fluffy pink-white frosting mound
    ctx.fillStyle = '#fff0f5';
    ctx.beginPath();
    ctx.arc(-5, 0, 7, 0, Math.PI * 2);
    ctx.arc(5, 0, 7, 0, Math.PI * 2);
    ctx.arc(0, -6, 8, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#ff6ebe';
    ctx.beginPath();
    ctx.arc(0, -7, 4.5, 0, Math.PI * 2);
    ctx.fill();

    // Glistening ruby cherry on top
    ctx.fillStyle = '#ff1144';
    ctx.shadowBlur = 0;
    ctx.beginPath();
    ctx.arc(0, -13, 3.5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-1, -15, 1.5, 1.5);

    ctx.restore();
  }

  function drawCosmicPinata(ctx, p) {
    ctx.save();
    ctx.translate(p.x, p.y);

    const tilt = Math.sin(p.bobPhase * 1.8) * 0.12 + (p.wobble ? Math.sin(p.bobPhase * 16) * 0.18 : 0);
    ctx.rotate(tilt);

    const isFlashing = p.hitFlash > 0;

    // 1. Rainbow Streamers trailing from bottom
    const streamerCols = ['#ff007f', '#ffd700', '#00f0ff', '#76ff03'];
    for (let s = 0; s < 4; s++) {
      const sx = -24 + s * 16;
      const wave = Math.sin(p.bobPhase * 2 + s * 1.2) * 12;
      ctx.strokeStyle = streamerCols[s];
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(sx, 16);
      ctx.quadraticCurveTo(sx + wave * 0.5, 34, sx + wave, 52);
      ctx.stroke();
    }

    // 2. Twin Jet Thrusters
    const jetGlow1 = ctx.createRadialGradient(-18, 18, 2, -18, 26, 12);
    jetGlow1.addColorStop(0, '#00ffff');
    jetGlow1.addColorStop(1, 'transparent');
    ctx.fillStyle = jetGlow1;
    ctx.beginPath(); ctx.arc(-18, 24, 12, 0, Math.PI * 2); ctx.fill();

    const jetGlow2 = ctx.createRadialGradient(18, 18, 2, 18, 26, 12);
    jetGlow2.addColorStop(0, '#00ffff');
    jetGlow2.addColorStop(1, 'transparent');
    ctx.fillStyle = jetGlow2;
    ctx.beginPath(); ctx.arc(18, 24, 12, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = isFlashing ? '#ffffff' : '#3a2560';
    ctx.fillRect(-22, 12, 8, 7);
    ctx.fillRect(14, 12, 8, 7);

    // 3. Main Saucer Disk (Piñata Fringe Layers)
    const aura = ctx.createRadialGradient(0, 0, 15, 0, 0, 54);
    aura.addColorStop(0, isFlashing ? 'rgba(255, 255, 255, 0.95)' : 'rgba(255, 215, 0, 0.45)');
    aura.addColorStop(0.7, 'rgba(255, 0, 128, 0.2)');
    aura.addColorStop(1, 'transparent');
    ctx.fillStyle = aura;
    ctx.beginPath(); ctx.ellipse(0, 2, 54, 28, 0, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = isFlashing ? '#ffffff' : '#220f45';
    ctx.beginPath(); ctx.ellipse(0, 4, 46, 20, 0, 0, Math.PI * 2); ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = isFlashing ? '#ffff00' : '#ffd700';
    ctx.stroke();

    const fringeLayers = [
      { col: '#ff007f', y: 8, rx: 42, ry: 13 },
      { col: '#ff9900', y: 3, rx: 39, ry: 11 },
      { col: '#ffd700', y: -2, rx: 36, ry: 10 },
      { col: '#00f0ff', y: -6, rx: 32, ry: 9 }
    ];

    fringeLayers.forEach(fl => {
      ctx.fillStyle = isFlashing ? '#ffffff' : fl.col;
      ctx.beginPath();
      ctx.ellipse(0, fl.y, fl.rx, fl.ry, 0, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = isFlashing ? '#ffffaa' : '#ffffff';
      ctx.globalAlpha = 0.35;
      for (let f = -fl.rx + 6; f < fl.rx - 6; f += 8) {
        ctx.fillRect(f, fl.y - 1, 4, 3);
      }
      ctx.globalAlpha = 1.0;
    });

    // Glowing dome canopy
    const domeGrad = ctx.createRadialGradient(-6, -18, 3, 0, -12, 24);
    domeGrad.addColorStop(0, isFlashing ? '#ffffff' : 'rgba(255, 255, 255, 0.95)');
    domeGrad.addColorStop(0.3, 'rgba(120, 240, 255, 0.85)');
    domeGrad.addColorStop(0.8, 'rgba(180, 0, 255, 0.65)');
    domeGrad.addColorStop(1, 'rgba(40, 10, 80, 0.9)');
    ctx.fillStyle = domeGrad;
    ctx.beginPath();
    ctx.ellipse(0, -10, 24, 18, 0, Math.PI, 0);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#00f0ff';
    ctx.stroke();

    // Inside dome: Mini Birthday Cake Pilot!
    ctx.fillStyle = '#ff6ebe';
    ctx.beginPath(); ctx.arc(0, -12, 7, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-1.5, -21, 3, 6);
    ctx.fillStyle = '#ffd700';
    ctx.beginPath(); ctx.arc(0, -23, 2.5, 0, Math.PI * 2); ctx.fill();

    // Party Hat on top of UFO
    ctx.fillStyle = '#ff007f';
    ctx.beginPath();
    ctx.moveTo(0, -38);
    ctx.lineTo(-8, -24);
    ctx.lineTo(8, -24);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#ffd700';
    ctx.beginPath(); ctx.arc(0, -39, 3.5, 0, Math.PI * 2); ctx.fill();

    ctx.restore();

    // Floating HP Shield Bar above Piñata
    const barW = 84;
    const barH = 9;
    const barX = p.x - barW / 2;
    const barY = p.y - 48;

    ctx.save();
    ctx.fillStyle = 'rgba(10, 5, 25, 0.85)';
    ctx.strokeStyle = '#ffd700';
    ctx.lineWidth = 1.5;
    if (ctx.roundRect) ctx.roundRect(barX, barY, barW, barH, 4);
    else ctx.fillRect(barX, barY, barW, barH);
    ctx.fill();
    ctx.stroke();

    const segW = (barW - 4) / p.maxHp;
    for (let s = 0; s < p.maxHp; s++) {
      if (s < p.hp) {
        ctx.fillStyle = s < 2 ? '#ff2a55' : (s < 4 ? '#ffd700' : '#00ff88');
        ctx.fillRect(barX + 2 + s * segW + 0.5, barY + 2, segW - 1, barH - 4);
      }
    }

    ctx.fillStyle = '#ffd700';
    ctx.font = '7px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.shadowColor = '#000';
    ctx.shadowBlur = 4;
    ctx.fillText("🛸 GOLDEN PIÑATA", p.x, barY - 4);
    ctx.restore();
  }

  function drawBouncingCake(ctx, bc) {
    ctx.save();
    ctx.translate(bc.x, bc.y);
    ctx.rotate(bc.rot);

    const trailGrad = ctx.createRadialGradient(0, 10, 1, 0, 18, 14);
    trailGrad.addColorStop(0, 'rgba(255, 215, 0, 0.85)');
    trailGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = trailGrad;
    ctx.beginPath(); ctx.arc(0, 14, 14, 0, Math.PI * 2); ctx.fill();

    // Tier 1 (bottom)
    ctx.fillStyle = '#ff6ebe';
    ctx.fillRect(-12, 0, 24, 10);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-12, -2, 24, 3);

    // Tier 2 (top)
    ctx.fillStyle = '#ffd700';
    ctx.fillRect(-8, -10, 16, 9);
    ctx.fillStyle = '#ff007f';
    ctx.fillRect(-8, -11, 16, 2.5);

    // Lit candle
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(-1.5, -18, 3, 7);
    ctx.fillStyle = '#ff3300';
    ctx.beginPath(); ctx.arc(0, -20, 3, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ffff00';
    ctx.beginPath(); ctx.arc(0, -21, 1.8, 0, Math.PI * 2); ctx.fill();

    ctx.restore();
  }

  function drawStarCandy(ctx, x, y, rot, fl_t) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);

    const aura = ctx.createRadialGradient(0, 0, 3, 0, 0, 22);
    aura.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
    aura.addColorStop(0.4, 'rgba(255, 215, 0, 0.85)');
    aura.addColorStop(1, 'transparent');
    ctx.fillStyle = aura;
    ctx.beginPath(); ctx.arc(0, 0, 22, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = '#ffd700';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {
      const a1 = (i * 72 - 90) * Math.PI / 180;
      const a2 = (i * 72 + 36 - 90) * Math.PI / 180;
      const r1 = 15;
      const r2 = 7;
      if (i === 0) ctx.moveTo(Math.cos(a1) * r1, Math.sin(a1) * r1);
      else ctx.lineTo(Math.cos(a1) * r1, Math.sin(a1) * r1);
      ctx.lineTo(Math.cos(a2) * r2, Math.sin(a2) * r2);
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#220033';
    ctx.fillRect(-4, -2, 2, 3);
    ctx.fillRect(2, -2, 2, 3);
    ctx.beginPath(); ctx.arc(0, 2, 2.5, 0, Math.PI); ctx.stroke();

    ctx.restore();
  }

  function drawGoldenMacaron(ctx, x, y, rot) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);

    ctx.fillStyle = '#ffd700';
    ctx.beginPath(); ctx.ellipse(0, -4, 15, 7, 0, Math.PI, 0); ctx.fill();
    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1; ctx.stroke();

    ctx.fillStyle = '#ff007f';
    ctx.fillRect(-14, -4, 28, 5);

    ctx.fillStyle = '#ffd700';
    ctx.beginPath(); ctx.ellipse(0, 1, 15, 7, 0, 0, Math.PI); ctx.fill();
    ctx.stroke();

    ctx.restore();
  }

  function drawSugarGem(ctx, x, y, rot, fl_t) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);

    const aura = ctx.createRadialGradient(0, 0, 2, 0, 0, 18);
    aura.addColorStop(0, 'rgba(0, 255, 255, 0.9)');
    aura.addColorStop(1, 'transparent');
    ctx.fillStyle = aura;
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = '#00f0ff';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, -14);
    ctx.lineTo(13, 0);
    ctx.lineTo(0, 14);
    ctx.lineTo(-13, 0);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(0, -14);
    ctx.lineTo(5, 0);
    ctx.lineTo(0, -4);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }

  function drawPinataFrenzyBanner(ctx) {
    ctx.save();
    const bannerW = Math.min(WIDTH - 32, 490);
    const bannerH = 46;
    const bannerX = WIDTH / 2 - bannerW / 2;
    const bannerY = 82;

    const pulse = Math.sin(globalTime * 8) * 0.2 + 0.8;
    ctx.shadowColor = '#ffd700';
    ctx.shadowBlur = 20 * pulse;

    const bgGrad = ctx.createLinearGradient(bannerX, bannerY, bannerX + bannerW, bannerY + bannerH);
    bgGrad.addColorStop(0, 'rgba(35, 10, 50, 0.95)');
    bgGrad.addColorStop(0.5, 'rgba(70, 15, 60, 0.95)');
    bgGrad.addColorStop(1, 'rgba(35, 10, 50, 0.95)');
    ctx.fillStyle = bgGrad;
    if (ctx.roundRect) ctx.roundRect(bannerX, bannerY, bannerW, bannerH, 12);
    else ctx.fillRect(bannerX, bannerY, bannerW, bannerH);
    ctx.fill();

    ctx.strokeStyle = ['#ffd700', '#ff007f', '#00f0ff', '#76ff03'][Math.floor(globalTime * 6) % 4];
    ctx.lineWidth = 2.5;
    if (ctx.roundRect) ctx.roundRect(bannerX, bannerY, bannerW, bannerH, 12);
    else ctx.strokeRect(bannerX, bannerY, bannerW, bannerH);
    ctx.stroke();

    ctx.fillStyle = '#ffd700';
    ctx.font = 'bold 9px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText("🛸 COSMIC PIÑATA FRENZY! 🍬", WIDTH / 2, bannerY + 16);

    const barW = bannerW - 60;
    const barH = 8;
    const barX = WIDTH / 2 - barW / 2;
    const barY2 = bannerY + 25;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    ctx.fillRect(barX, barY2, barW, barH);

    const pct = Math.max(0, pinataFrenzyTime / 10.0);
    const fillGrad = ctx.createLinearGradient(barX, barY2, barX + barW, barY2);
    fillGrad.addColorStop(0, '#ff007f');
    fillGrad.addColorStop(0.5, '#ffd700');
    fillGrad.addColorStop(1, '#00f0ff');
    ctx.fillStyle = fillGrad;
    ctx.fillRect(barX, barY2, barW * pct, barH);

    ctx.fillStyle = '#ffffff';
    ctx.font = '7px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`${pinataFrenzyTime.toFixed(1)}s`, WIDTH / 2, barY2 + 7);

    ctx.restore();
  }

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
      if (p.drag) {
        const factor = Math.max(0, 1 - p.drag * dt);
        p.vx *= factor;
        p.vy *= factor;
      }
      if (p.gravity) {
        p.vy += p.gravity * dt;
      }
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

      // Power-up & Fortune timers
      if (slowmoTime > 0) slowmoTime -= dt;
      if (fortuneTimer > 0) fortuneTimer -= dt;
      if (starFeverTime > 0) {
        starFeverTime -= dt;
        // Extra rainbow stardust while Star-Fever is active
        if (Math.random() < 0.4) {
          trails.push({
            x: player.x + (Math.random() - 0.5) * 40,
            y: player.y - 40 + (Math.random() - 0.5) * 20,
            vy: -20,
            life: 0.6,
            color: ['#ffd700', '#ff0077', '#00dcff', '#70e000'][Math.floor(Math.random() * 4)]
          });
        }
      }

      // Player Movement (responsive drag + keys + buttons)
      let moveDir = 0;
      if (keys['ArrowLeft'] || keys['KeyA']) moveDir -= 1;
      if (keys['ArrowRight'] || keys['KeyD']) moveDir += 1;

      // Compute player velocity & bank tilt
      const curX = player.x;

      // Phone Tilt Steering (deadzone of 3.0 degrees)
      let tiltSteerFactor = 0;
      if (tiltMode && Math.abs(currentTiltAngle) > 3.0) {
        const sign = currentTiltAngle > 0 ? 1 : -1;
        const mag = Math.min(1.0, (Math.abs(currentTiltAngle) - 3.0) / 22.0);
        tiltSteerFactor = sign * mag;
      }

      if (moveDir !== 0) {
        player.x += moveDir * player.speed * dt;
        targetX = player.x;
        player.walkTime += dt * 10;
      } else if (tiltSteerFactor !== 0) {
        player.x += tiltSteerFactor * player.speed * 1.25 * dt;
        targetX = player.x;
        player.walkTime += Math.abs(tiltSteerFactor) * dt * 10;
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
        const isBad = (pinataFrenzyTime > 0) ? false : (Math.random() < Math.min(0.45, 0.28 + (stage - 1) * 0.006));
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
          if (starFeverTime > 0) {
            // Star-Fever transforms falling hazards into edible golden cupcakes!
            items.push({
              x: hw.x,
              y: -35,
              vy: hw.vy * 0.9,
              isBad: false,
              isPowerup: false,
              isCupcake: true,
              kind: 'CUPCAKE',
              pts: 100,
              rot: 0,
              vrot: (Math.random() - 0.5) * 3,
              color: COLORS.GOLD
            });
          } else {
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
          }
          hazardWarnings.splice(w, 1);
        }
      }

      // Rare Birthday Shooting Star Spawner (~every 28s)
      starSpawnTimer -= dt;
      if (starSpawnTimer <= 0) {
        starSpawnTimer = 26.0 + Math.random() * 12.0;
        const minX = Math.min(90, WIDTH * 0.12);
        const maxX = WIDTH - minX;
        items.push({
          x: minX + Math.random() * (maxX - minX),
          y: -40,
          vy: speed * 0.72,
          isBad: false,
          isPowerup: false,
          isShootingStar: true,
          kind: 'SHOOTING_STAR',
          pts: 250,
          rot: 0,
          vrot: 3.4,
          color: '#ffd700'
        });
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

      // Cosmic Piñata UFO Update (Stages 9, 19, 29)
      if (pinata.active) {
        pinata.bobPhase += dt * 3.5;
        pinata.hitFlash = Math.max(0, pinata.hitFlash - dt * 3.5);
        pinata.wobble = Math.max(0, pinata.wobble - dt * 2.5);
        pinata.x += pinata.vx * dt;
        pinata.y = 115 + Math.sin(pinata.bobPhase) * 14;

        if (pinata.x > WIDTH - 55 && pinata.vx > 0) {
          pinata.vx = -Math.abs(pinata.vx);
        } else if (pinata.x < 55 && pinata.vx < 0) {
          pinata.vx = Math.abs(pinata.vx);
        }

        if (Math.random() < 0.5) {
          trails.push({
            x: pinata.x + (Math.random() - 0.5) * 36,
            y: pinata.y + 12,
            vy: 25 + Math.random() * 25,
            life: 0.45,
            color: ['#ff007f', '#ffd700', '#00e5ff', '#76ff03'][Math.floor(Math.random() * 4)]
          });
        }
      }

      // Update Bouncing Cakes & check Piñata collision
      for (let b = bouncingCakes.length - 1; b >= 0; b--) {
        const bc = bouncingCakes[b];
        bc.x += bc.vx * dt;
        bc.y += bc.vy * dt;
        bc.vy += 160 * dt;
        bc.rot += bc.vrot * dt;

        if (Math.random() < 0.45) {
          particles.push({
            x: bc.x,
            y: bc.y,
            vx: (Math.random() - 0.5) * 20,
            vy: (Math.random() - 0.5) * 20,
            size: 2,
            color: '#ffd700',
            life: 0.25,
            maxLife: 0.25
          });
        }

        if (pinata.active && Math.abs(bc.x - pinata.x) < 55 && Math.abs(bc.y - pinata.y) < 38) {
          bouncingCakes.splice(b, 1);
          pinata.hp--;
          pinata.hitFlash = 1.0;
          pinata.wobble = 0.4;
          sfxCatch();
          playTone(880, 'square', 0.12, 0.25);
          haptic([35, 45]);
          addCollectBurst(pinata.x, pinata.y, '#ffd700');
          addScorePopup(pinata.x, pinata.y - 25, `PIÑATA HIT! ${pinata.hp}/${pinata.maxHp}`, '#ffd700');

          if (pinata.hp <= 0) {
            pinata.cracked = true;
            pinata.active = false;
            score += 1000;
            pinataFrenzyTime = 10.0;
            frenzySpawnTimer = 0;
            sfxStarFever();
            haptic([50, 70, 50, 70, 120]);
            for (let fw = 0; fw < 4; fw++) {
              addFireworks(pinata.x + (fw - 1.5) * 45, pinata.y - 20, ['#ffd700', '#ff007f', '#00f0ff', '#76ff03'][fw]);
            }
            addCollectBurst(pinata.x, pinata.y, '#ffd700');
            addCollectBurst(pinata.x, pinata.y, '#ff007f');
            addScorePopup(WIDTH / 2, HEIGHT / 2 - 50, "🎉 COSMIC PIÑATA CRACKED! +1000", '#ffd700');
            toastFortune("🛸 Golden Piñata Unleashed Sweet Cascade! 🍬", 4.0);

            items.forEach(it => {
              if (it.isBad) {
                it.isBad = false;
                it.isCupcake = true;
                it.kind = 'CUPCAKE';
                it.pts = 100;
                it.color = COLORS.GOLD;
                addCollectBurst(it.x, it.y, '#ffd700');
              }
            });
            hazardWarnings = [];
          }
          continue;
        }

        if (bc.y < -60 || bc.y > HEIGHT + 60 || bc.x < -60 || bc.x > WIDTH + 60) {
          bouncingCakes.splice(b, 1);
        }
      }

      // 10-Second Sweet Cascade Bonus Frenzy
      if (pinataFrenzyTime > 0) {
        pinataFrenzyTime -= dt;
        hazardWarnings = [];

        frenzySpawnTimer -= dt;
        if (frenzySpawnTimer <= 0) {
          frenzySpawnTimer = 0.22;
          const minX = Math.min(80, WIDTH * 0.12);
          const maxX = WIDTH - minX;
          const fx = minX + Math.random() * (maxX - minX);
          const fKinds = ['STAR_CANDY', 'GOLDEN_MACARON', 'SUGAR_GEM'];
          const fk = fKinds[Math.floor(Math.random() * fKinds.length)];
          items.push({
            x: fx,
            y: -30,
            vy: speed * 1.15,
            isBad: false,
            isPowerup: false,
            isFrenzyTreat: true,
            kind: fk,
            pts: 100,
            rot: 0,
            vrot: (Math.random() - 0.5) * 4.5,
            color: fk === 'STAR_CANDY' ? '#ffd700' : (fk === 'GOLDEN_MACARON' ? '#ff6ebe' : '#00ffff')
          });
        }
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

            // If on Piñata stage, bounce a cake skyward toward the Cosmic Piñata!
            if ((stage === 9 || stage === 19 || stage === 29) && pinata.active) {
              bouncingCakes.push({
                x: player.x,
                y: trayRect.y - 10,
                vx: (Math.random() - 0.5) * 60 + player.vx * 0.22,
                vy: -520,
                rot: 0,
                vrot: (Math.random() - 0.5) * 6
              });
              playTone(587, 'sine', 0.08, 0.2);
            }

            if (item.isShootingStar) {
              // Catch Rare Birthday Shooting Star -> Activate 5s Rainbow Star-Fever!
              starFeverTime = 5.0;
              score += 250;
              sfxStarFever();
              haptic([40, 50, 40, 50, 100]);
              addScorePopup(player.x, player.y - 80, "⭐ STAR-FEVER! +250", '#ffd700');
              addCollectBurst(item.x, item.y, '#ffd700');

              // Instantly transform ALL existing hazards into golden cupcakes!
              items.forEach(it => {
                if (it.isBad) {
                  it.isBad = false;
                  it.isCupcake = true;
                  it.kind = 'CUPCAKE';
                  it.pts = 100;
                  it.color = COLORS.GOLD;
                  addCollectBurst(it.x, it.y, '#ffd700');
                }
              });
              hazardWarnings = [];
              items.splice(i, 1);
            } else if (item.isFrenzyTreat) {
              score += 100;
              itemsCaughtStage++;
              comboStreak++;
              addCollectBurst(item.x, item.y, '#ffd700');
              addScorePopup(item.x, item.y - 20, "+100 FRENZY!", '#ffd700');
              sfxCatch();
              haptic(20);
              items.splice(i, 1);
            } else if (item.isCupcake) {
              // Catch Transformed Golden Cupcake!
              score += 100;
              itemsCaughtStage++;
              comboStreak++;
              addCollectBurst(item.x, item.y, '#ffd700');
              addScorePopup(item.x, item.y - 20, "+100 CUPCAKE!", '#ffd700');
              sfxCatch();
              haptic(20);
              items.splice(i, 1);
            } else if (item.isPowerup) {
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
          // Obstacle collision (Aisha is completely invincible during Star-Fever and Piñata Frenzy)
          if (player.invincible <= 0 && starFeverTime <= 0 && pinataFrenzyTime <= 0) {
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
          if (!item.isBad && !item.isPowerup && !item.isFrenzyTreat) {
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
        if (Math.random() < 0.07) {
          const fx = 100 + Math.random() * (WIDTH - 200);
          const fy = 80 + Math.random() * (HEIGHT * 0.45);
          const randShape = Math.random();
          if (randShape < 0.35) {
            addHeartFireworks(fx, fy);
          } else if (randShape < 0.70) {
            addStarFireworks(fx, fy);
          } else {
            addLetterFireworks(fx, fy, AISHA_SEQUENCE[Math.floor(Math.random() * AISHA_SEQUENCE.length)]);
          }
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
      else if (item.kind === 'SHOOTING_STAR') drawShootingStar(ctx, item.x, item.y, item.rot, globalTime);
      else if (item.kind === 'CUPCAKE') drawCupcake(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'STAR_CANDY') drawStarCandy(ctx, item.x, item.y, item.rot, globalTime);
      else if (item.kind === 'GOLDEN_MACARON') drawGoldenMacaron(ctx, item.x, item.y, item.rot);
      else if (item.kind === 'SUGAR_GEM') drawSugarGem(ctx, item.x, item.y, item.rot, globalTime);
      ctx.restore();
    });

    // Bouncing Cakes flying towards Piñata
    bouncingCakes.forEach(bc => drawBouncingCake(ctx, bc));

    // Cosmic Birthday Piñata UFO (Stages 9, 19, 29)
    if (pinata.active && state === 'PLAYING') {
      drawCosmicPinata(ctx, pinata);
    }

    // Sweet Cascade Piñata Frenzy Banner
    if (pinataFrenzyTime > 0 && state === 'PLAYING') {
      drawPinataFrenzyBanner(ctx);
    }

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
      // Keep Aisha 100% solid and fully visible during Star-Fever and Frenzy (never disappears like a ghost)
      const flicker = (starFeverTime <= 0 && pinataFrenzyTime <= 0) && player.invincible > 0 && Math.floor(player.invincible * 14) % 2 === 0;
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

        // Rainbow Star-Fever Aura around Aisha
        if (starFeverTime > 0) {
          ctx.save();
          const rCols = ['#ff0077', '#00dcff', '#ffd700', '#70e000', '#bd00ff'];
          const rCol = rCols[Math.floor(globalTime * 12) % rCols.length];
          ctx.shadowColor = rCol;
          ctx.shadowBlur = 25;
          ctx.strokeStyle = rCol;
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.arc(0, -32, 74 + Math.sin(globalTime * 14) * 4, 0, Math.PI * 2);
          ctx.stroke();

          ctx.fillStyle = rCol;
          ctx.globalAlpha = 0.15;
          ctx.fill();
          ctx.restore();
        }

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
        const fSize = p.fontSize || 13;
        ctx.font = fSize + 'px "Press Start 2P", monospace';
        ctx.textAlign = 'center';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = Math.max(2, Math.round(fSize / 4));
        ctx.strokeText(p.text, 0, 0);
        ctx.shadowColor = p.glowColor || p.color;
        ctx.shadowBlur = p.glow || 10;
        ctx.fillText(p.text, 0, 0);
      } else {
        if (p.trail && p.vx !== undefined && p.vy !== undefined) {
          ctx.strokeStyle = p.color;
          ctx.globalAlpha = alpha * 0.5;
          ctx.lineWidth = Math.max(1.5, p.size * 0.8);
          ctx.beginPath();
          ctx.moveTo(p.x - p.vx * 0.035, p.y - p.vy * 0.035);
          ctx.lineTo(p.x, p.y);
          ctx.stroke();
        }
        ctx.fillStyle = p.color;
        ctx.globalAlpha = alpha;
        if (p.glow) {
          ctx.shadowColor = p.glowColor || p.color;
          ctx.shadowBlur = p.glow;
        }
        if (p.shape === 'star') {
          drawStarShape(ctx, p.x, p.y, 5, p.size * 1.5, p.size * 0.65);
          ctx.fill();
        } else if (p.shape === 'heart') {
          drawHeartShape(ctx, p.x, p.y, p.size * 1.6);
          ctx.fill();
        } else if (p.shape === 'sparkle') {
          const s = p.size * 1.4;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y - s);
          ctx.lineTo(p.x + s * 0.35, p.y);
          ctx.lineTo(p.x, p.y + s);
          ctx.lineTo(p.x - s * 0.35, p.y);
          ctx.closePath();
          ctx.fill();
        } else {
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      ctx.restore();
    });

    // ─── RETRO 16-BIT HUD ─────────────────────────────────────────────
    // Top Score Box — Sharp Bright Yellow, indented past gear button
    ctx.save();
    ctx.fillStyle = '#ffd700';
    ctx.shadowColor = 'rgba(255, 215, 0, 0.6)';
    ctx.shadowBlur = 8;
    ctx.font = '13px "Press Start 2P", monospace';
    ctx.textAlign = 'left';
    ctx.fillText("SCORE: " + String(score).padStart(6, "0"), pw + 72, safeTop + 14);
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
    ctx.font = '15px "Press Start 2P", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(tStr, WIDTH / 2, safeTop + 14);
    ctx.restore();

    // Mini Cake Level Progress Bar (0 to 20 ingredients)
    const progW = 120;
    const progH = 6;
    const progX = WIDTH / 2 - progW / 2;
    const progY = safeTop + 24;
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

    // Birthday Fortune Toast Banner
    if (fortuneTimer > 0 && state === 'PLAYING') {
      ctx.save();
      const fAlpha = Math.min(1.0, fortuneTimer / 0.5);
      ctx.globalAlpha = fAlpha;
      const boxW = Math.min(WIDTH - 40, 520);
      const boxH = 46;
      const boxX = WIDTH / 2 - boxW / 2;
      const boxY = safeTop + 86;

      ctx.fillStyle = 'rgba(15, 8, 38, 0.94)';
      ctx.shadowColor = '#ffd700';
      ctx.shadowBlur = 18;
      if (ctx.roundRect) ctx.roundRect(boxX, boxY, boxW, boxH, 12);
      else ctx.fillRect(boxX, boxY, boxW, boxH);
      ctx.fill();

      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 2.5;
      if (ctx.roundRect) ctx.roundRect(boxX, boxY, boxW, boxH, 12);
      else ctx.strokeRect(boxX, boxY, boxW, boxH);
      ctx.stroke();

      ctx.fillStyle = '#ffd700';
      ctx.font = 'bold 9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText("🎁 BIRTHDAY TOAST UNLOCKED! 🎁", WIDTH / 2, boxY + 16);

      ctx.fillStyle = '#ffffff';
      ctx.font = '8px "Press Start 2P", monospace';
      ctx.fillText(activeFortuneText, WIDTH / 2, boxY + 34);
      ctx.restore();
    }

    // Active Power-up Badges in HUD
    let puY = safeTop + 54;
    if (pinataFrenzyTime > 0) {
      ctx.fillStyle = '#ffd700';
      ctx.shadowColor = '#ffd700';
      ctx.shadowBlur = 10;
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`🛸 SWEET FRENZY (${Math.ceil(pinataFrenzyTime)}s)`, WIDTH / 2, puY);
      ctx.shadowBlur = 0;
      puY += 15;
    }
    if (starFeverTime > 0) {
      ctx.fillStyle = '#ffd700';
      ctx.shadowColor = '#ffd700';
      ctx.shadowBlur = 8;
      ctx.font = '9px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`⭐ STAR-FEVER (${Math.ceil(starFeverTime)}s)`, WIDTH / 2, puY);
      ctx.shadowBlur = 0;
      puY += 15;
    }
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

    // Pixel Hearts (Lives) — Top Right, indented past pause button
    const hx = WIDTH - pw - 72;
    for (let i = 0; i < MAX_LIVES; i++) {
      const active = i < lives;
      const lx = hx - (MAX_LIVES - 1 - i) * 26;
      ctx.save();
      ctx.fillStyle = active ? '#ff2a55' : '#331520';
      if (active) {
        ctx.shadowColor = '#ff2a55';
        ctx.shadowBlur = 8;
      }
      ctx.fillRect(lx - 10, safeTop + 5, 9, 9);
      ctx.fillRect(lx - 1, safeTop + 5, 9, 9);
      ctx.fillRect(lx - 9, safeTop + 14, 16, 7);
      ctx.fillRect(lx - 5, safeTop + 21, 8, 4);
      if (active) {
        ctx.fillStyle = '#ffb3c6';
        ctx.fillRect(lx - 8, safeTop + 7, 3, 3);
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
    ctx.fillText("ZERO-G MODE", pw + 18, HEIGHT - safeBottom - 8);
    ctx.restore();

    // Gyroscope / Tilt Steering Horizon Bubble Indicator
    if (tiltMode && state === 'PLAYING') {
      ctx.save();
      const tIndW = 86;
      const tIndH = 14;
      const tIndX = WIDTH / 2 - tIndW / 2;
      const tIndY = HEIGHT - safeBottom - 18;

      ctx.fillStyle = 'rgba(8, 14, 38, 0.88)';
      ctx.strokeStyle = '#00dcff';
      ctx.lineWidth = 1.5;
      if (ctx.roundRect) ctx.roundRect(tIndX, tIndY, tIndW, tIndH, 7);
      else ctx.strokeRect(tIndX, tIndY, tIndW, tIndH);
      ctx.fill();
      ctx.stroke();

      ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
      ctx.beginPath();
      ctx.moveTo(WIDTH / 2, tIndY + 2);
      ctx.lineTo(WIDTH / 2, tIndY + tIndH - 2);
      ctx.stroke();

      const tiltNorm = Math.max(-1, Math.min(1, currentTiltAngle / 26));
      const bubbleX = WIDTH / 2 + tiltNorm * (tIndW / 2 - 8);
      ctx.fillStyle = Math.abs(tiltNorm) > 0.12 ? '#ffd700' : '#00dcff';
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(bubbleX, tIndY + tIndH / 2, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#00dcff';
      ctx.font = '6px "Press Start 2P", monospace';
      ctx.textAlign = 'center';
      ctx.shadowBlur = 0;
      ctx.fillText("📳 TILT ON", WIDTH / 2, tIndY - 4);
      ctx.restore();
    } else {
      // Animated Neon Sine Wave Oscillation
      ctx.strokeStyle = '#00dcff';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      const waveStart = pw + 180;
      const waveWidth = Math.max(100, WIDTH - pw * 2 - 370);
      for (let wx = 0; wx < waveWidth; wx += 4) {
        const wy = HEIGHT - safeBottom - 11 + Math.sin(wx * 0.08 + globalTime * 7) * 7;
        if (wx === 0) ctx.moveTo(waveStart + wx, wy);
        else ctx.lineTo(waveStart + wx, wy);
      }
      ctx.stroke();
    }

    ctx.save();
    ctx.fillStyle = '#ff9900';
    ctx.shadowColor = '#ffaa00';
    ctx.shadowBlur = 10;
    ctx.font = '13px "Press Start 2P", monospace';
    ctx.textAlign = 'right';
    ctx.fillText("STAGE " + stage + "/" + TOTAL_STAGES, WIDTH - pw - 18, HEIGHT - safeBottom - 8);

    const costumeTitle = stage >= 30 ? "💎 TIARA" : (stage >= 20 ? "🧑‍🍳 CHEF" : (stage >= 10 ? "👑 CROWN" : "🎀 PARTY"));
    ctx.fillStyle = stage >= 30 ? '#00f0ff' : (stage >= 20 ? '#ffffff' : (stage >= 10 ? '#ffd700' : '#ff6ebe'));
    ctx.font = '8px "Press Start 2P", monospace';
    ctx.fillText(costumeTitle, WIDTH - pw - 18, HEIGHT - safeBottom - 22);
    ctx.restore();

    // ─── OVERLAY SCREENS ──────────────────────────────────────────────
    const boxW = Math.min(WIDTH - 36, 680);
    const boxH = Math.min(HEIGHT - 120, 420);

    if (state === 'MENU') {
      btnAction.textContent = 'START';
      const boxW = Math.min(WIDTH - 32, 640);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 520);
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
      ctx.fillText("★ AISHA'S ★", WIDTH / 2, boxY + 34);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '15px "Press Start 2P", monospace';
      ctx.fillText("BIRTHDAY BAKE-OFF!", WIDTH / 2, boxY + 60);

      // Centerpiece Portrait of Aisha (Floating 16-bit framed portrait)
      const floatY = Math.sin(globalTime * 2.2) * 5;
      const portH = Math.min(210, Math.round(boxH * 0.42));
      const portW = Math.round(portH * 0.75);
      const portY = boxY + 70 + portH / 2;
      drawAishaPortrait(ctx, WIDTH / 2, portY, portW, portH, floatY);

      // Birthday Girl Ribbon Tag
      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("★ THE BIRTHDAY GIRL ★", WIDTH / 2, portY + portH / 2 + 18 + floatY);

      // Checkpoint resume option or new game prompt
      if (checkpointStage > 1) {
        ctx.fillStyle = COLORS.CYAN;
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.fillText(`★ CHECKPOINT: STAGE ${checkpointStage} (${checkpointScore.toLocaleString()} PTS) ★`, WIDTH / 2, boxY + boxH - 100);

        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '12px "Press Start 2P", monospace';
        ctx.fillText(`★ TAP TO RESUME STAGE ${checkpointStage} ★`, WIDTH / 2, boxY + boxH - 72);
      } else {
        ctx.fillStyle = '#c8d4f0';
        ctx.font = '10px "Press Start 2P", monospace';
        ctx.fillText("CATCH FALLING CAKES - DODGE ANVILS!", WIDTH / 2, boxY + boxH - 100);

        const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
        ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
        ctx.font = '14px "Press Start 2P", monospace';
        ctx.fillText("▶ TAP SCREEN TO PLAY ◀", WIDTH / 2, boxY + boxH - 72);
      }

      ctx.fillStyle = '#859bb8';
      ctx.font = '8px "Press Start 2P", monospace';
      ctx.fillText(`BEST: ${hiScore.toLocaleString()}   |   🛸 BONUS PIÑATA: LVL 9, 19, 29`, WIDTH / 2, boxY + boxH - 42);
      ctx.fillStyle = '#ff94c2';
      ctx.font = '7px "Press Start 2P", monospace';
      ctx.fillText("★ ⚙️ QUICK SETTINGS FOR 🏆 HALL OF FAME ★", WIDTH / 2, boxY + boxH - 18);
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
      const boxW = Math.min(WIDTH - 24, 660);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 30, 540);
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
        // Mystery Presents Gacha Section (Right after blowing out candles!)
        if (presentGachaActive) {
          presents.forEach(p => {
            const floatY = Math.sin(globalTime * 3.5 + p.floatOffset) * 6;
            const py = p.y + floatY;

            ctx.save();
            ctx.translate(p.x, py);

            if (!p.opened) {
              // Box glow
              ctx.shadowColor = p.colors.ribbon;
              ctx.shadowBlur = 12 + Math.sin(globalTime * 5 + p.floatOffset) * 6;

              // Box base
              ctx.fillStyle = p.colors.box;
              ctx.fillRect(-35, -20, 70, 55);
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 2;
              ctx.strokeRect(-35, -20, 70, 55);

              // Vertical ribbon
              ctx.fillStyle = p.colors.ribbon;
              ctx.fillRect(-8, -20, 16, 55);

              // Horizontal ribbon
              ctx.fillRect(-35, 2, 70, 14);

              // Lid
              ctx.fillStyle = p.colors.lid;
              ctx.fillRect(-40, -32, 80, 15);
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 1.5;
              ctx.strokeRect(-40, -32, 80, 15);

              // Top Satin Bow Loops
              ctx.fillStyle = p.colors.ribbon;
              ctx.beginPath();
              ctx.ellipse(-12, -38, 12, 7, -0.3, 0, Math.PI * 2);
              ctx.fill();
              ctx.beginPath();
              ctx.ellipse(12, -38, 12, 7, 0.3, 0, Math.PI * 2);
              ctx.fill();
              ctx.beginPath();
              ctx.arc(0, -36, 5, 0, Math.PI * 2);
              ctx.fill();

              // Box Label
              ctx.shadowBlur = 0;
              ctx.fillStyle = '#ffffff';
              ctx.font = '8px "Press Start 2P", monospace';
              ctx.textAlign = 'center';
              ctx.fillText("TAP ME 🎁", 0, 48);
            } else {
              // Opened Box!
              const rayGrad = ctx.createLinearGradient(0, -20, 0, -120);
              rayGrad.addColorStop(0, 'rgba(255, 215, 0, 0.85)');
              rayGrad.addColorStop(1, 'rgba(255, 215, 0, 0)');
              ctx.fillStyle = rayGrad;
              ctx.beginPath();
              ctx.moveTo(-35, -10);
              ctx.lineTo(-75, -110);
              ctx.lineTo(75, -110);
              ctx.lineTo(35, -10);
              ctx.closePath();
              ctx.fill();

              // Box base
              ctx.fillStyle = p.colors.box;
              ctx.fillRect(-35, -15, 70, 50);
              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 2;
              ctx.strokeRect(-35, -15, 70, 50);

              // Vertical ribbon
              ctx.fillStyle = p.colors.ribbon;
              ctx.fillRect(-8, -15, 16, 50);

              // Lid popped off and tilted!
              ctx.save();
              ctx.translate(-25, -45);
              ctx.rotate(-0.4);
              ctx.fillStyle = p.colors.lid;
              ctx.fillRect(-38, -8, 76, 14);
              ctx.restore();

              // Floating star badge above box
              ctx.fillStyle = '#ffd700';
              ctx.shadowColor = '#ffd700';
              ctx.shadowBlur = 16;
              ctx.font = '22px sans-serif';
              ctx.textAlign = 'center';
              ctx.fillText("👑", 0, -50);
            }
            ctx.restore();
          });
        }

        if (!presentGachaOpened) {
          ctx.fillStyle = COLORS.GOLD;
          ctx.font = '10px "Press Start 2P", monospace';
          ctx.fillText("★ BIRTHDAY WISH GRANTED! ★", WIDTH / 2, boxY + 418);

          const pulse = Math.floor(globalTime * 3) % 2 === 0;
          ctx.fillStyle = pulse ? '#ffd700' : '#ffffff';
          ctx.font = '10px "Press Start 2P", monospace';
          ctx.fillText("🎁 TAP A MYSTERY PRESENT TO UNBOX! 🎁", WIDTH / 2, boxY + 440);

          ctx.fillStyle = '#ff6ebe';
          ctx.font = '8px "Press Start 2P", monospace';
          ctx.fillText("✨ TOUCH SKY FOR 💖 ⭐ 🔤 FIREWORKS! ✨", WIDTH / 2, boxY + 462);

          ctx.fillStyle = '#ff6ebe';
          ctx.font = '9px "Press Start 2P", monospace';
          ctx.fillText("📸 [ TAP HERE TO DECORATE POLAROID ]", WIDTH / 2, boxY + 490);

          ctx.fillStyle = '#859bb8';
          ctx.font = '8px "Press Start 2P", monospace';
          ctx.fillText(`${info.bonus}   |   SCORE: ${score.toLocaleString()}`, WIDTH / 2, boxY + 520);
        } else {
          ctx.fillStyle = COLORS.GOLD;
          ctx.font = '10.5px "Press Start 2P", monospace';
          ctx.fillText(`★ UNBOXED: ${gachaWonBadge} ★`, WIDTH / 2, boxY + 414);

          ctx.fillStyle = '#00f0ff';
          ctx.font = '9px "Press Start 2P", monospace';
          ctx.fillText(`PERK: ${gachaWonPerk.perkName}`, WIDTH / 2, boxY + 434);

          ctx.fillStyle = '#ffffff';
          ctx.font = '8px "Press Start 2P", monospace';
          ctx.fillText(gachaWonPerk.desc, WIDTH / 2, boxY + 452);

          const advPrompt = (stage < TOTAL_STAGES) ? `▶ TAP TO ADVANCE TO LEVEL ${stage + 1} ◀` : "★ TAP TO PLAY AGAIN ★";
          const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
          ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
          ctx.font = '11px "Press Start 2P", monospace';
          ctx.fillText(advPrompt, WIDTH / 2, boxY + 478);

          ctx.fillStyle = '#ff6ebe';
          ctx.font = '9px "Press Start 2P", monospace';
          ctx.fillText("📸 [ TAP HERE TO DECORATE POLAROID ]", WIDTH / 2, boxY + 504);

          ctx.fillStyle = '#859bb8';
          ctx.font = '7.5px "Press Start 2P", monospace';
          ctx.fillText(`VERIFIED BIRTHDAY EDITION   |   SCORE: ${score.toLocaleString()}`, WIDTH / 2, boxY + 528);
        }
      }
    } else if (state === 'GAME_OVER') {
      btnAction.textContent = 'RETRY';
      const boxW = Math.min(WIDTH - 32, 640);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 520);
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
      ctx.fillText("CAKE DISASTER!", WIDTH / 2, boxY + 36);

      // Aisha Portrait on game over
      const portH = Math.min(170, Math.round(boxH * 0.36));
      const portW = Math.round(portH * 0.75);
      const portY = boxY + 54 + portH / 2;
      drawAishaPortrait(ctx, WIDTH / 2, portY, portW, portH, 0);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '10px "Press Start 2P", monospace';
      ctx.fillText("DON'T GIVE UP ON AISHA'S CAKE!", WIDTH / 2, portY + portH / 2 + 16);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("Score: " + score.toLocaleString(), WIDTH / 2, boxY + boxH - 110);
      ctx.fillStyle = COLORS.GOLD;
      ctx.fillText("Hi-Score: " + hiScore.toLocaleString(), WIDTH / 2, boxY + boxH - 86);

      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("▶ TAP TO RETRY ◀", WIDTH / 2, boxY + boxH - 62);

      ctx.fillStyle = '#ff6ebe';
      ctx.font = '8.5px "Press Start 2P", monospace';
      ctx.fillText("📸 TAP TO SHARE POLAROID CERTIFICATE 📸", WIDTH / 2, boxY + boxH - 36);

      ctx.fillStyle = '#859bb8';
      ctx.font = '7px "Press Start 2P", monospace';
      ctx.fillText("★ ⚙️ QUICK SETTINGS FOR 🏆 HALL OF FAME ★", WIDTH / 2, boxY + boxH - 16);
    } else if (state === 'WIN') {
      btnAction.textContent = 'AGAIN';
      const boxW = Math.min(WIDTH - 32, 660);
      const boxH = Math.min(HEIGHT - safeTop - safeBottom - 40, 530);
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
      ctx.fillText("★ GRAND CHAMPION BAKER! ★", WIDTH / 2, boxY + 34);

      ctx.fillStyle = COLORS.PINK;
      ctx.font = '14px "Press Start 2P", monospace';
      ctx.fillText("HAPPY BIRTHDAY AISHA! 🎂", WIDTH / 2, boxY + 58);

      ctx.fillStyle = '#ff6ebe';
      ctx.font = '7.5px "Press Start 2P", monospace';
      ctx.fillText("✨ TOUCH OR DRAG SKY FOR 💖 ⭐ 🔤 FIREWORKS! ✨", WIDTH / 2, boxY + 76);

      const floatY = Math.sin(globalTime * 2.2) * 5;
      const portH = Math.min(200, Math.round(boxH * 0.40));
      const portW = Math.round(portH * 0.75);
      const portY = boxY + 88 + portH / 2;
      drawAishaPortrait(ctx, WIDTH / 2, portY, portW, portH, floatY);

      ctx.fillStyle = COLORS.GOLD;
      ctx.font = '10px "Press Start 2P", monospace';
      ctx.fillText("★ ALL 30 LEVELS CONQUERED! ★", WIDTH / 2, portY + portH / 2 + 16 + floatY);

      ctx.fillStyle = COLORS.WHITE;
      ctx.font = '11px "Press Start 2P", monospace';
      ctx.fillText("FINAL SCORE: " + score.toLocaleString(), WIDTH / 2, boxY + boxH - 96);

      const pulse = Math.floor(globalTime * 2.5) % 2 === 0;
      ctx.fillStyle = pulse ? COLORS.CYAN_GLOW : COLORS.WHITE;
      ctx.font = '13px "Press Start 2P", monospace';
      ctx.fillText("★ TAP TO PLAY AGAIN ★", WIDTH / 2, boxY + boxH - 68);

      ctx.fillStyle = '#ff6ebe';
      ctx.font = '8.5px "Press Start 2P", monospace';
      ctx.fillText("📸 TAP TO SHARE POLAROID CERTIFICATE 📸", WIDTH / 2, boxY + boxH - 42);

      ctx.fillStyle = '#859bb8';
      ctx.font = '8px "Press Start 2P", monospace';
      ctx.fillText("BEST: " + hiScore.toLocaleString(), WIDTH / 2, boxY + boxH - 22);

      ctx.fillStyle = '#ff94c2';
      ctx.font = '7px "Press Start 2P", monospace';
      ctx.fillText("★ ⚙️ QUICK SETTINGS FOR 🏆 HALL OF FAME ★", WIDTH / 2, boxY + boxH - 6);
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

with open("assets/aisha_candid.jpg", "rb") as f:
    candid_b64 = base64.b64encode(f.read()).decode("ascii")

with open("assets/aisha_head.png", "rb") as f:
    head_b64 = base64.b64encode(f.read()).decode("ascii")

with open("assets/icon-192.png", "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("ascii")

html = html.replace("%%AISHA_PORTRAIT_B64%%", portrait_b64)
html = html.replace("%%AISHA_CANDID_B64%%", candid_b64)
html = html.replace("%%AISHA_HEAD_B64%%", head_b64)
html = html.replace("%%AISHA_ICON_B64%%", icon_b64)

with open("game.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully compiled ultra-quality retro pixel game.html with Aisha centerpiece! Size:", len(html))
