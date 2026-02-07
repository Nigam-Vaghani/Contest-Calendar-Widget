# Contest Calendar Widget

## Problem I Noticed

While regularly participating in competitive programming contests, I realized that keeping track of contest schedules was unnecessarily annoying.

Most of the time, I had to:
- Open Codeforces or LeetCode repeatedly
- Check which contest is coming
- Remember whether it’s Div 2, Div 3, or a LeetCode contest
- Keep mental notes about dates and times

Even after checking, I would still forget because the information wasn’t visible where I actually spend my time — the desktop.

I wanted something simple:
A small calendar on my desktop that quietly shows contest days, so I don’t need to think about it.

That’s where this project started.

---

## Idea

The idea was straightforward.

If contest schedules are already published online,  
why not display them directly on the desktop in a clean and readable way?

Instead of reminders, notifications, or browser tabs,  
I wanted a passive widget that:

- Always stays visible
- Shows contest dates clearly
- Differentiates platforms visually
- Gives full contest details only when I hover

No distractions. No manual checking.

---

## What This Project Does

This is a desktop calendar widget built using Python and PyQt6.

It fetches upcoming contests from:
- Codeforces
- LeetCode

And displays them directly inside a floating calendar window.

Each contest day is visually highlighted so that at a glance, I can tell:
- Which days have contests
- Which platform the contest belongs to
- Whether today has a contest

Hovering over a date shows detailed information like:
- Platform
- Contest type
- Time
- Contest name

---

## Features

- Floating desktop calendar widget
- Always-on-top window
- Glass-style UI with rounded corners and shadows
- Platform-based color highlighting
- Special visual treatment for today’s date
- Smooth hover animations on dates
- Tooltip with full contest details
- Draggable window
- Lightweight and fast

---

## Project Structure

```
Contest-Calendar-Widget/
│
├── main.py
├── ui/
│   └── widget_window.py
├── data/
│   └── contest_fetcher.py
├── calender/
│   └── calender_logic.py
├── requirements.txt
└── README.md
```

---

## How to Run (For Developers)

1. Clone the repository

```bash
git clone https://github.com/<your-username>/Contest-Calendar-Widget.git
cd Contest-Calendar-Widget
```

2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python main.py
```

---

## Download (For Users)

A compiled Windows executable is available in the Releases section of the GitHub repository.

Windows may show a warning saying the app is not commonly downloaded. This happens because the application is unsigned. You can safely choose “Run anyway”.

---

## Why This Exists

With this widget:
- I don’t forget contests
- I don’t need to check multiple websites
- Contest information is always visible but never distracting

It solves a small problem, but one that I personally faced every week.

---

## Future Improvements

- Month navigation
- Remember window position
- More platforms
- Auto-start on system boot
- Cross-platform builds

---

## Author

Nigam Vaghani

Computer Science student  
Interested in desktop UI, systems, and practical problem-solving

---

## License

MIT License
