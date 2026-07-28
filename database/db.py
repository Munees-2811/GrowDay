"""
TaskFlow Database Module
========================
SQLite database operations for tasks, habits, categories, and timer.
"""

import sqlite3
import os
from datetime import datetime, date, timedelta


DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "taskflow.db")


def get_connection():
    """Create and return a database connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_database():
    """Create all required tables and seed defaults if they don't exist."""
    conn = get_connection()
    try:
        # ── Tasks ────────────────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority TEXT DEFAULT 'Medium',
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                is_recurring INTEGER DEFAULT 0,
                category_id INTEGER,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        """)

        # ── Habits ───────────────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                frequency TEXT DEFAULT 'Every day',
                target_count INTEGER DEFAULT 1,
                color TEXT DEFAULT '#E91E63',
                icon TEXT DEFAULT '⬛',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                log_date TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
                UNIQUE(habit_id, log_date)
            )
        """)

        # ── Categories ───────────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT DEFAULT '📁',
                color TEXT DEFAULT '#E91E63',
                is_default INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)

        # ── Timer Records ────────────────────────────────────────────
        conn.execute("""
            CREATE TABLE IF NOT EXISTS timer_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity TEXT DEFAULT '',
                duration_seconds INTEGER DEFAULT 0,
                timer_type TEXT DEFAULT 'Stopwatch',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)

        conn.commit()

        # Seed default categories if table is empty
        count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        if count == 0:
            defaults = [
                ("Art", "🎨", "#E040FB", 1),
                ("Task", "🕐", "#FF5722", 1),
                ("Meditation", "🧘", "#9C27B0", 1),
                ("Study", "🎓", "#7C4DFF", 1),
                ("Sports", "🚴", "#00BCD4", 1),
                ("Entertainment", "🎬", "#26C6DA", 1),
                ("Health", "💊", "#4CAF50", 1),
                ("Work", "💼", "#FF9800", 1),
            ]
            conn.executemany(
                "INSERT INTO categories (name, icon, color, is_default) VALUES (?, ?, ?, ?)",
                defaults,
            )
            conn.commit()

    finally:
        conn.close()


# =========================================================================
#  Task CRUD
# =========================================================================

def add_task(title, description="", priority="Medium", due_date=None, is_recurring=0, category_id=None):
    """Insert a new task and return its id."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, priority, due_date, is_recurring, category_id) VALUES (?, ?, ?, ?, ?, ?)",
            (title, description, priority, due_date, is_recurring, category_id),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_tasks(recurring=None):
    """Return tasks, optionally filtered by recurring status."""
    conn = get_connection()
    try:
        if recurring is not None:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE is_recurring = ? ORDER BY created_at DESC", (1 if recurring else 0,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_task_by_id(task_id):
    """Return a single task by its id, or None."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_tasks_by_date(target_date):
    """Return tasks whose due_date matches target_date (YYYY-MM-DD)."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE due_date = ? ORDER BY completed ASC, priority DESC",
            (target_date,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_today_tasks():
    """Return tasks due today."""
    return get_tasks_by_date(date.today().isoformat())


def get_upcoming_tasks():
    """Return incomplete tasks with a future due date."""
    today = date.today().isoformat()
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE due_date > ? AND completed = 0 ORDER BY due_date ASC",
            (today,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_overdue_tasks():
    """Return incomplete tasks whose due date has passed."""
    today = date.today().isoformat()
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE due_date < ? AND completed = 0 AND due_date IS NOT NULL ORDER BY due_date ASC",
            (today,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_completed_tasks():
    """Return all completed tasks."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE completed = 1 ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_task(task_id, title, description, priority, due_date, is_recurring=0, category_id=None):
    """Update an existing task."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE tasks SET title=?, description=?, priority=?, due_date=?, is_recurring=?, category_id=? WHERE id=?",
            (title, description, priority, due_date, is_recurring, category_id, task_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_task(task_id):
    """Delete a task by id."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    finally:
        conn.close()


def mark_task_completed(task_id, completed=True):
    """Toggle the completed status of a task."""
    conn = get_connection()
    try:
        conn.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
        conn.commit()
    finally:
        conn.close()


def get_task_stats():
    """Return aggregate task statistics."""
    conn = get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1").fetchone()[0]
        pending = total - completed
        today_str = date.today().isoformat()
        today_total = conn.execute("SELECT COUNT(*) FROM tasks WHERE due_date = ?", (today_str,)).fetchone()[0]
        today_done = conn.execute("SELECT COUNT(*) FROM tasks WHERE due_date = ? AND completed = 1", (today_str,)).fetchone()[0]
        overdue = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE due_date < ? AND completed = 0 AND due_date IS NOT NULL",
            (today_str,),
        ).fetchone()[0]
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "today_total": today_total,
            "today_completed": today_done,
            "today_pending": today_total - today_done,
            "overdue": overdue,
            "completion_rate": round((completed / total) * 100, 1) if total else 0.0,
            "today_completion_rate": round((today_done / today_total) * 100, 1) if today_total else 0.0,
        }
    finally:
        conn.close()


# =========================================================================
#  Habit CRUD
# =========================================================================

def add_habit(name, description="", frequency="Every day", color="#E91E63", icon="⬛"):
    """Insert a new habit."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO habits (name, description, frequency, color, icon) VALUES (?, ?, ?, ?, ?)",
            (name, description, frequency, color, icon),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_habits():
    """Return all habits."""
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM habits ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_habit_by_id(habit_id):
    """Return a single habit."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_habit(habit_id, name, description="", frequency="Every day", color="#E91E63", icon="⬛"):
    """Update a habit."""
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE habits SET name=?, description=?, frequency=?, color=?, icon=? WHERE id=?",
            (name, description, frequency, color, icon, habit_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_habit(habit_id):
    """Delete a habit and its logs."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
    finally:
        conn.close()


def log_habit(habit_id, log_date=None):
    """Mark a habit as done for a given date (default: today)."""
    if log_date is None:
        log_date = date.today().isoformat()
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
            (habit_id, log_date),
        )
        conn.commit()
    finally:
        conn.close()


def unlog_habit(habit_id, log_date=None):
    """Remove a habit log for a given date."""
    if log_date is None:
        log_date = date.today().isoformat()
    conn = get_connection()
    try:
        conn.execute(
            "DELETE FROM habit_logs WHERE habit_id = ? AND log_date = ?",
            (habit_id, log_date),
        )
        conn.commit()
    finally:
        conn.close()


def is_habit_done(habit_id, log_date=None):
    """Check if a habit is logged for a given date."""
    if log_date is None:
        log_date = date.today().isoformat()
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ? AND log_date = ?",
            (habit_id, log_date),
        ).fetchone()
        return row[0] > 0
    finally:
        conn.close()


def get_habit_week_status(habit_id, end_date=None):
    """Return a list of 7 dicts [{date, day_name, done}] for the week ending on end_date."""
    if end_date is None:
        end_date = date.today()
    elif isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    start_date = end_date - timedelta(days=6)
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT log_date FROM habit_logs WHERE habit_id = ? AND log_date BETWEEN ? AND ?",
            (habit_id, start_date.isoformat(), end_date.isoformat()),
        ).fetchall()
        done_dates = {r["log_date"] for r in rows}

        week = []
        for i in range(7):
            d = start_date + timedelta(days=i)
            week.append({
                "date": d,
                "day_name": d.strftime("%a"),
                "day_num": d.day,
                "done": d.isoformat() in done_dates,
                "is_today": d == date.today(),
                "is_future": d > date.today(),
            })
        return week
    finally:
        conn.close()


def get_habit_streak(habit_id):
    """Return the current streak (consecutive days done ending today or yesterday)."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT log_date FROM habit_logs WHERE habit_id = ? ORDER BY log_date DESC",
            (habit_id,),
        ).fetchall()
        if not rows:
            return 0

        dates = [date.fromisoformat(r["log_date"]) for r in rows]
        streak = 0
        check = date.today()
        # Allow starting from today or yesterday
        if dates[0] == check:
            pass
        elif dates[0] == check - timedelta(days=1):
            check = check - timedelta(days=1)
        else:
            return 0

        for d in dates:
            if d == check:
                streak += 1
                check -= timedelta(days=1)
            elif d < check:
                break
        return streak
    finally:
        conn.close()


def get_habit_completion_rate(habit_id):
    """Return completion percentage based on days since habit creation."""
    conn = get_connection()
    try:
        habit = conn.execute("SELECT created_at FROM habits WHERE id = ?", (habit_id,)).fetchone()
        if not habit:
            return 0
        created = datetime.fromisoformat(habit["created_at"]).date()
        total_days = max((date.today() - created).days + 1, 1)
        done_count = conn.execute(
            "SELECT COUNT(*) FROM habit_logs WHERE habit_id = ?", (habit_id,)
        ).fetchone()[0]
        return min(round((done_count / total_days) * 100), 100)
    finally:
        conn.close()


# =========================================================================
#  Category CRUD
# =========================================================================

def get_all_categories(default_only=None):
    """Return categories, optionally filtered."""
    conn = get_connection()
    try:
        if default_only is True:
            rows = conn.execute("SELECT * FROM categories WHERE is_default = 1 ORDER BY name").fetchall()
        elif default_only is False:
            rows = conn.execute("SELECT * FROM categories WHERE is_default = 0 ORDER BY created_at DESC").fetchall()
        else:
            rows = conn.execute("SELECT * FROM categories ORDER BY is_default ASC, name ASC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_category(name, icon="📁", color="#E91E63"):
    """Add a custom category."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO categories (name, icon, color, is_default) VALUES (?, ?, ?, 0)",
            (name, icon, color),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def delete_category(cat_id):
    """Delete a custom category."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM categories WHERE id = ? AND is_default = 0", (cat_id,))
        conn.commit()
    finally:
        conn.close()


def get_category_entry_count(cat_id):
    """Count tasks + habits assigned to a category."""
    conn = get_connection()
    try:
        count = conn.execute("SELECT COUNT(*) FROM tasks WHERE category_id = ?", (cat_id,)).fetchone()[0]
        return count
    finally:
        conn.close()


# =========================================================================
#  Timer Records
# =========================================================================

def add_timer_record(activity, duration_seconds, timer_type="Stopwatch"):
    """Save a timer record."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO timer_records (activity, duration_seconds, timer_type) VALUES (?, ?, ?)",
            (activity, duration_seconds, timer_type),
        )
        conn.commit()
    finally:
        conn.close()


def get_recent_timer_records(limit=10):
    """Return recent timer records."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM timer_records ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
