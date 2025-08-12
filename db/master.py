import sqlite3, os

DB_PATH = os.getenv("DB_PATH","./db/jobs.db")

def init_db(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT, company TEXT, location TEXT, url TEXT,
                match_score REAL, relocation_detected INTEGER, date_added TEXT
            )
        """)

def is_new_job(sig, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute("SELECT 1 FROM jobs WHERE id=?", (sig,))
        return cur.fetchone() is None

def save_job(sig, job, db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO jobs (id,title,company,location,url,match_score,relocation_detected,date_added) VALUES (?,?,?,?,?,?,?,datetime('now'))",
            (sig, job['title'], job['company'], job.get('location',''), job['url'], job['match_score'], int(job['relocation_detected']))
        )
