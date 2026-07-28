"""
TaskFlow Utility Helpers
========================
Date formatting, week strip, SVG generators, timer formatting.
"""

from datetime import datetime, date, timedelta


# ── Greetings ────────────────────────────────────────────────────────────

def get_greeting():
    """Return a time-of-day greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    elif hour < 21:
        return "Good Evening"
    return "Good Night"


# ── Date helpers ─────────────────────────────────────────────────────────

def format_date(d, fmt="%B %d, %Y"):
    """Format a date (or ISO string) for display."""
    if d is None:
        return "No date"
    if isinstance(d, str):
        try:
            d = date.fromisoformat(d)
        except ValueError:
            return d
    return d.strftime(fmt)


def get_week_dates(center_date=None):
    """
    Return 7 date dicts centered around center_date (default: today).
    Each dict: {date, day_name, day_num, is_today, is_selected}.
    """
    if center_date is None:
        center_date = date.today()
    elif isinstance(center_date, str):
        center_date = date.fromisoformat(center_date)

    # Start from 3 days before center
    start = center_date - timedelta(days=3)
    week = []
    for i in range(7):
        d = start + timedelta(days=i)
        week.append({
            "date": d,
            "day_name": d.strftime("%a"),
            "day_num": d.day,
            "is_today": d == date.today(),
        })
    return week


# ── Priority helpers ─────────────────────────────────────────────────────

def priority_color(priority):
    """Return a hex colour for a priority level."""
    return {
        "High": "#EF4444",
        "Medium": "#F59E0B",
        "Low": "#4CAF50",
    }.get(priority, "#6B7280")


def priority_icon(priority):
    """Return an emoji for a priority level."""
    return {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")


def days_remaining(due_date_str):
    """Human-readable 'days until due' label."""
    if not due_date_str:
        return ""
    try:
        due = date.fromisoformat(due_date_str)
    except ValueError:
        return ""
    delta = (due - date.today()).days
    if delta < 0:
        return f"Overdue by {abs(delta)}d"
    if delta == 0:
        return "Due today"
    if delta == 1:
        return "Due tomorrow"
    return f"{delta}d left"


# ── SVG helpers ──────────────────────────────────────────────────────────

def habit_circle_svg(day_num, done=False, is_today=False, is_future=False, size=36):
    """
    Generate an SVG circle for a habit day.
    - done → green filled
    - is_today & not done → pink outline
    - future → gray outline
    - past & not done → dark gray filled
    """
    r = size // 2 - 2
    cx = cy = size // 2

    if done:
        fill = "#4CAF50"
        stroke = "#4CAF50"
        text_color = "#fff"
    elif is_today:
        fill = "transparent"
        stroke = "#E91E63"
        text_color = "#E91E63"
    elif is_future:
        fill = "transparent"
        stroke = "#444"
        text_color = "#666"
    else:
        fill = "#2A2A3A"
        stroke = "#2A2A3A"
        text_color = "#888"

    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:inline-block;margin:0 2px;">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>
        <text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central"
              fill="{text_color}" font-size="{size//3}" font-weight="700">{day_num}</text>
    </svg>"""


def timer_ring_svg(elapsed_pct=0, size=220):
    """
    Generate a circular timer ring SVG.
    elapsed_pct: 0.0 to 1.0
    """
    cx = cy = size // 2
    r = size // 2 - 12
    circumference = 2 * 3.14159 * r
    offset = circumference * (1 - elapsed_pct)

    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="display:block;margin:0 auto;">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2A2A3A" stroke-width="8"/>
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#E91E63" stroke-width="8"
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                stroke-linecap="round" transform="rotate(-90 {cx} {cy})"
                style="transition: stroke-dashoffset 0.5s ease;"/>
    </svg>"""


# ── Timer formatting ────────────────────────────────────────────────────

def format_timer(seconds):
    """Format seconds into MM:SS or HH:MM:SS."""
    seconds = max(0, int(seconds))
    if seconds >= 3600:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"
