import sqlite3
from dataclasses import dataclass
import os

def upgrade_if_needed():
    '''
    Checks the database's schema version (pragma user_version), and upgrades the database if needed
    '''
    db = sqlite3.connect(
        "db/db.db", detect_types=sqlite3.PARSE_DECLTYPES
    )
    version = db.execute("PRAGMA user_version").fetchone()
    print(version)
    scripts = os.listdir("db_upgrade_scripts")
    for script in scripts:
        scriptver = script[:-4]
        if int(scriptver) >= version[0]:
            print("upgrading using " + script)
            with open("db_upgrade_scripts/" + script) as f:
                db.executescript(f.read())

    db.commit()

            

if __name__ == "__main__":
    upgrade_if_needed()