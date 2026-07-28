# ⚡ TaskFlow (GrowDay)

> **A modern productivity application** — Task Manager + Habit Tracker + Daily Planner — built with Python & Streamlit.

---

## 🚀 Features (v1.0)

| Feature | Status |
|---------|--------|
| **Home Dashboard** — greeting, stats cards, quick-add task | ✅ |
| **Task Management** — full CRUD with priority, due dates, tabs | ✅ |
| **Habits Page** — placeholder UI | 🔜 |
| **Calendar Page** — date picker + tasks by date | ✅ |
| **Statistics Page** — totals, completion rate bar | ✅ |
| **Settings** — dark mode, display name, notifications | ✅ |
| **SQLite Storage** — local, zero-config database | ✅ |
| **Custom CSS** — dark/light theme, mobile-first responsive | ✅ |

---

## 📁 Project Structure

```
TaskFlow/
│
├── app.py                 # Main entry point
├── requirements.txt       # Python dependencies
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   └── db.py              # SQLite CRUD operations
│
├── pages/
│   ├── __init__.py
│   ├── tasks.py            # Task management page
│   ├── habits.py           # Habits placeholder page
│   ├── calendar.py         # Calendar page
│   └── statistics.py       # Statistics / analytics page
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py          # Sidebar navigation
│   ├── task_card.py        # Reusable task card
│   └── habit_card.py       # Reusable habit card (placeholder)
│
├── utils/
│   ├── __init__.py
│   └── helpers.py          # Date, greeting, priority helpers
│
└── data/
    └── taskflow.db         # SQLite database (auto-created)
```

---

## ⚙️ Installation

### Prerequisites

- **Python 3.11+** (3.10 minimum)
- **pip** package manager

### Steps

```bash
# 1. Clone or navigate to the project
cd TaskFlow

# 2. (Recommended) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** by default.

### 📱 Access from Mobile (Same Network)

1. Find your PC's local IP address:
   ```bash
   ipconfig    # Windows
   # ifconfig  # macOS / Linux
   ```
2. Open your mobile browser and navigate to:
   ```
   http://<YOUR_PC_IP>:8501
   ```
   > Both devices must be on the **same Wi-Fi network**.

---

## 🗄️ Database

TaskFlow uses **SQLite** — a lightweight, file-based SQL database that requires zero configuration.

- **Location:** `data/taskflow.db`
- **Created automatically** on first run.
- **Tables:**
  | Table | Purpose |
  |-------|---------|
  | `tasks` | Stores all tasks with title, description, priority, due date, completion status |
  | `habits` | Stores habit definitions (future use) |
  | `habit_logs` | Logs daily habit completions (future use) |

All database operations are in `database/db.py`.

---

## 🧪 Testing Checklist

| # | Test | How |
|---|------|-----|
| 1 | Home page loads | Navigate to Home in sidebar |
| 2 | Sidebar navigation | Click each nav item |
| 3 | Add a task | Use Quick Add on Home or + Add New Task on Tasks page |
| 4 | View tasks | Open Tasks page → All tab |
| 5 | Complete a task | Click ✅ Complete on a task card |
| 6 | Edit a task | Click ✏️ Edit, change values, save |
| 7 | Delete a task | Click 🗑️ Delete on a task card |
| 8 | Calendar shows tasks | Pick a date with tasks on the Calendar page |
| 9 | Stats reflect data | Check Statistics page metrics |
| 10 | Dark mode | Toggle in Settings |

---

## 🛠️ Build / Deploy

### Local Desktop
Run with `streamlit run app.py`.

### Streamlit Community Cloud
1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Deploy from GitHub.

### Android APK (Future)
The long-term goal is to package this as an Android APK using tools like **Kivy + Buildozer** or a WebView wrapper. Instructions will be added when that milestone is reached.

---

## 📄 License

This project is for personal / educational use. Feel free to modify and extend it.
>>>>>>> d3be687 (Initial commit - TaskFlow mobile productivity app)
