import sqlite3

db = sqlite3.connect(
    "database.sqlite",
    check_same_thread=False
)

cursor = db.cursor()

# =========================
# TABELA TICKETS
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    user_id INTEGER,
    canal_id INTEGER
)
""")

# =========================
# TABELA LIVES
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS lives (
    user_id INTEGER,
    msg_id INTEGER
)
""")

# =========================
# TABELA CONTRATOS
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS contratos (
    user_id INTEGER,
    nivel TEXT
)
""")

db.commit()