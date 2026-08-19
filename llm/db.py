import sqlite3

DB_NAME = "mcp_store.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS page_locators(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        page_name TEXT,
        element_name TEXT UNIQUE,
        primary_locator TEXT,
        healed_locator TEXT,
        last_verified TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_locator(page_name, element_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT healed_locator, primary_locator 
        FROM page_locators
        WHERE page_name=? AND element_name=?
    """, (page_name, element_name))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    healed, primary = row
    return healed if healed else primary


def upsert_locator(page_name, element_name, primary_locator, healed_locator, timestamp):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO page_locators(page_name, element_name, primary_locator, healed_locator, last_verified)
        VALUES(?,?,?,?,?)
        ON CONFLICT(element_name)
        DO UPDATE SET
           healed_locator=excluded.healed_locator,
           last_verified=excluded.last_verified
    """, (page_name, element_name, primary_locator, healed_locator, timestamp))

    conn.commit()
    conn.close()
