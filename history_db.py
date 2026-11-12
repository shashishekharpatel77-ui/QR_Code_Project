import sqlite3
from datetime import datetime

import config


def connect():
    return sqlite3.connect(config.Db_Path)


def init_db():
    conn = connect()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS history ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "qr_type TEXT, data TEXT, created_at TEXT)"
    )
    conn.commit()
    conn.close()


def add_history(qr_type, data):
    conn = connect()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO history (qr_type, data, created_at) VALUES (?, ?, ?)",
        (qr_type, data, now),
    )
    conn.commit()
    conn.close()


def get_history(limit=50):
    conn = connect()
    rows = conn.execute(
        "SELECT qr_type, data, created_at FROM history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows