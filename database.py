import sqlite3

# Connect to database
def connect_db():
    return sqlite3.connect("workflow.db")


# ---------------- TASKS TABLE ----------------

def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def add_task(name, priority):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (name, priority) VALUES (?, ?)",
        (name, priority)
    )

    conn.commit()
    conn.close()


def get_tasks():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def update_task(task_id, completed):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed=? WHERE id=?",
        (int(completed), task_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()


# ---------------- WORKFLOW HISTORY TABLE ----------------

def create_workflow_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_workflow(task, result):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO workflows (task, result) VALUES (?, ?)",
        (task, result)
    )

    conn.commit()
    conn.close()


def get_workflows():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM workflows ORDER BY id DESC"
    )

    workflows = cursor.fetchall()

    conn.close()

    return workflows


# ---------------- SCHEDULE PROGRESS TABLE ----------------

def create_schedule_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_name TEXT NOT NULL,
            activity TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Add schedule activity
def add_schedule_activity(schedule_name, activity):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO schedule_activities (schedule_name, activity)
        VALUES (?, ?)
        """,
        (schedule_name, activity)
    )

    conn.commit()
    conn.close()


# Get schedule activities
def get_schedule_activities():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM schedule_activities ORDER BY id DESC"
    )

    activities = cursor.fetchall()

    conn.close()

    return activities


# Update activity completion
def update_schedule_activity(activity_id, completed):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE schedule_activities SET completed=? WHERE id=?",
        (int(completed), activity_id)
    )

    conn.commit()
    conn.close()


# Delete schedule activity
def delete_schedule_activity(activity_id):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM schedule_activities WHERE id=?",
        (activity_id,)
    )

    conn.commit()
    conn.close()


# ---------------- CREATE ALL TABLES ----------------

create_table()
create_workflow_table()
create_schedule_table()