"""
TaskFlow Unit Tests
====================
Pytest unit tests for database CRUD operations and helper utilities.
"""

import os
import pytest
from datetime import date
from database.db import (
    initialize_database,
    add_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    mark_task_completed,
    add_habit,
    get_all_habits,
    delete_habit,
    get_all_categories,
)
from utils.helpers import get_greeting, format_date, priority_color


@pytest.fixture(autouse=True)
def setup_test_database(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    test_db = os.path.join(tmp_path, "test_taskflow.db")
    monkeypatch.setattr("database.db.DB_PATH", test_db)
    initialize_database()


def test_task_crud():
    """Test adding, retrieving, updating, and deleting tasks."""
    tid = add_task("Test Task", "Description", "High", date.today().isoformat())
    assert tid > 0

    task = get_task_by_id(tid)
    assert task is not None
    assert task["title"] == "Test Task"
    assert task["priority"] == "High"
    assert task["completed"] == 0

    # Mark completed
    mark_task_completed(tid, True)
    task = get_task_by_id(tid)
    assert task["completed"] == 1

    # Update task
    update_task(tid, "Updated Task", "New Desc", "Low", date.today().isoformat())
    task = get_task_by_id(tid)
    assert task["title"] == "Updated Task"
    assert task["priority"] == "Low"

    # Delete task
    delete_task(tid)
    assert get_task_by_id(tid) is None


def test_habit_crud():
    """Test habit creation and retrieval."""
    hid = add_habit("Read 10 mins", "Daily reading", "Every day", "#E91E63")
    assert hid > 0

    habits = get_all_habits()
    assert len(habits) >= 1
    assert any(h["name"] == "Read 10 mins" for h in habits)

    delete_habit(hid)
    habits_after = get_all_habits()
    assert not any(h["id"] == hid for h in habits_after)


def test_default_categories():
    """Test default categories seeding."""
    categories = get_all_categories()
    assert len(categories) >= 8
    cat_names = [c["name"] for c in categories]
    assert "Study" in cat_names
    assert "Sports" in cat_names


def test_helpers():
    """Test utility functions."""
    assert get_greeting() in ["Good Morning", "Good Afternoon", "Good Evening", "Good Night"]
    assert format_date("2026-07-28") == "July 28, 2026"
    assert priority_color("High") == "#EF4444"
