import sqlite3
from contextlib import closing

def connect_db():
    return sqlite3.connect("db.sqlite")

def init_db():
    with closing(connect_db()) as db:
        with open("schema.sql") as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == "__main__":
    init_db()
