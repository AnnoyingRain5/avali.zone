import os
import sqlite3


def upgrade_if_needed():
    """
    Checks the database's schema version (pragma user_version), and upgrades the database if needed
    """
    if not os.path.exists("db/db.db"):
        print("No database!!!")
        return
    db = sqlite3.connect("db/db.db", detect_types=sqlite3.PARSE_DECLTYPES)
    version = db.execute("PRAGMA user_version").fetchone()
    print(version)
    scripts = os.listdir("db_upgrade_scripts")
    scripts.sort()
    for script in scripts:
        script_version = script[:-4]
        if int(script_version) >= version[0]:
            print("upgrading using " + script)
            with open("db_upgrade_scripts/" + script) as f:
                db.executescript(f.read())

    db.commit()


if __name__ == "__main__":
    upgrade_if_needed()
