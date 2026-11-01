
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "patients.db"


def get_connection():
    """Create and return a SQLite database connection."""
    INSTANCE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    """Create the patients table if it does not exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT NOT NULL DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_all_patients():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM patients ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]


def get_patient(patient_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        ).fetchone()

    return dict(row) if row else None


def create_patient(data):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO patients (
                full_name, date_of_birth, email,
                glucose, haemoglobin, cholesterol, remarks
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["full_name"],
            data["date_of_birth"],
            data["email"],
            data["glucose"],
            data["haemoglobin"],
            data["cholesterol"],
            data.get("remarks", "")
        ))

        return cursor.lastrowid


def update_patient(patient_id, data):
    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE patients
            SET full_name = ?,
                date_of_birth = ?,
                email = ?,
                glucose = ?,
                haemoglobin = ?,
                cholesterol = ?,
                remarks = ?
            WHERE id = ?
        """, (
            data["full_name"],
            data["date_of_birth"],
            data["email"],
            data["glucose"],
            data["haemoglobin"],
            data["cholesterol"],
            data.get("remarks", ""),
            patient_id
        ))

        return cursor.rowcount > 0


def delete_patient(patient_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM patients WHERE id = ?",
            (patient_id,)
        )

        return cursor.rowcount > 0


def update_patient_remarks(patient_id, remarks):
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE patients SET remarks = ? WHERE id = ?",
            (remarks, patient_id)
        )
        return cursor.rowcount > 0
