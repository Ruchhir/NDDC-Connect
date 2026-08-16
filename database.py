import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path("data") / "wifi.db"


def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():
    """Create all required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # Users
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT NOT NULL,
        last_name TEXT,
        email TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_admin INTEGER DEFAULT 0
    )
    """)

    try:
      cursor.execute("""
        ALTER TABLE transactions
        ADD COLUMN mac_address TEXT DEFAULT 'PENDING'
    """)
    except:
     pass

    # Add email column to existing databases
    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN email TEXT
        """)
    except:
        pass

    # ==========================
    # Plans
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        duration_hours INTEGER NOT NULL,
        price INTEGER NOT NULL,
        max_devices INTEGER NOT NULL,
        speed_profile TEXT,
        active INTEGER DEFAULT 1
    )
    """)

# ==========================
# Transactions
# ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       telegram_id INTEGER NOT NULL,
       plan_id INTEGER NOT NULL,
       reference TEXT UNIQUE NOT NULL,
       amount INTEGER NOT NULL,
       status TEXT DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       paid_at TIMESTAMP
)
""")

    conn.commit()
    conn.close()

# =====================================================
# USERS
# =====================================================

def get_user(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def create_user(telegram_id, username, first_name, last_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (telegram_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        username,
        first_name,
        last_name
    ))

    conn.commit()
    conn.close()


# =====================================================
# PLANS
# =====================================================

def get_all_plans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM plans WHERE active = 1 ORDER BY price ASC"
    )

    plans = cursor.fetchall()

    conn.close()

    return plans


def get_plan(plan_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM plans WHERE id = ?",
        (plan_id,)
    )

    plan = cursor.fetchone()

    conn.close()

    return plan


# =====================================================
# SUBSCRIPTIONS
# =====================================================

def create_subscription(
    telegram_id,
    plan_id,
    start_date,
    end_date,
    status="active"
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subscriptions
        (
            telegram_id,
            plan_id,
            start_date,
            end_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        telegram_id,
        plan_id,
        start_date,
        end_date,
        status
    ))

    conn.commit()
    conn.close()


def get_subscription(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM subscriptions
        WHERE telegram_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (telegram_id,))

    subscription = cursor.fetchone()

    conn.close()

    return subscription

if __name__ == "__main__":
    plans = get_all_plans()

    for plan in plans:
        print(plan["id"], plan["name"])


def get_user_email(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE telegram_id = ?",
        (telegram_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return row["email"]

    return None


def save_user_email(telegram_id, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET email = ?
        WHERE telegram_id = ?
        """,
        (email, telegram_id),
    )

    conn.commit()
    conn.close()    

def create_transaction(
    telegram_id,
    plan_id,
    reference,
    amount,
    mac_address="PENDING",
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (
            telegram_id,
            plan_id,
            reference,
            amount,
            mac_address
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        telegram_id,
        plan_id,
        reference,
        amount,
        mac_address,
    ))

    conn.commit()
    conn.close()

def get_transaction(reference):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE reference = ?
    """, (reference,))

    row = cursor.fetchone()

    conn.close()

    return row

def mark_transaction_paid(reference):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET
            status='success',
            paid_at=CURRENT_TIMESTAMP
        WHERE reference=?
    """, (reference,))

    conn.commit()
    conn.close()