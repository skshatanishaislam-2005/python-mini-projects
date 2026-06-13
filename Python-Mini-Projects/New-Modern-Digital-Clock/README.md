# 🕐 LED Digital Clock — Modern Edition

A large-screen Python desktop clock with a 7-segment LED display style, built using Tkinter. Designed for MacBook M1 — opens at half screen size, perfectly centered.

## Preview

- Large purple glowing LED digits on a deep black background
- Blinking colons between hours, minutes, and seconds
- AM / PM indicator that lights up based on time
- Live date display showing day, month, and year
- SNOOZE button for the aesthetic
- Auto-centers on screen on every launch

## Features

- 12-hour format with AM/PM
- Large 7-segment digit rendering using Canvas
- Blinking colon animation every second
- Real-time date shown below the clock
- Auto-centered window at launch — no manual dragging
- Fully built with Python standard library — no pip installs needed

## Requirements

- Python 3.x
- Tkinter (comes built-in with Python)
- Works best on MacBook M1 (1440px wide display)

## How to Run

```bash
python New-Modern-Digital-Clock.py
```

## Project Structure

## How It Works

| Part | What it does |
|------|-------------|
| `draw_digit()` | Draws each number using 7 line segments on a Canvas |
| `SEGS` dictionary | Maps 0–9 to which segments should be ON or OFF |
| `tick()` | Updates all digits, colons, AM/PM, and date every 1000ms |
| `root.after()` | Schedules the next tick without freezing the window |
| `winfo_screenwidth()` | Detects screen size and centers the window automatically |

## Color Scheme

| Element | Color |
|---------|-------|
| Background | `#0a0a0a` (near black) |
| Active segments | `#e070ff` (purple / violet) |
| Dim segments | `#1e061e` (dark purple) |
| Date text | `#9940bb` (medium purple) |
| Active AM/PM | `#e070ff` on `#1f0a2a` |
| Inactive AM/PM | `#2a0a2a` on `#1a0a1a` |

## Window Size

| Setting | Value |
|---------|-------|
| Width | 1440px (half of MacBook M1 screen) |
| Height | 500px |
| Position | Auto-centered on launch |

## Built By

Tanisha 