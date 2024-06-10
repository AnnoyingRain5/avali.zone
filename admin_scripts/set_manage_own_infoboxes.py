import sqlite3

db = sqlite3.connect("db/db.db", detect_types=sqlite3.PARSE_DECLTYPES)

id = input("please enter the ID of the user you want to allow to manage their own infoboxes: ")
db.execute("UPDATE users SET manage_own_infoboxes = true WHERE id = ?", (id,))
db.commit()
print("Done!")
