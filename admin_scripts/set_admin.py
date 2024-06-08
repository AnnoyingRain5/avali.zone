import sqlite3

db = sqlite3.connect("db/db.db", detect_types=sqlite3.PARSE_DECLTYPES)

id = input("please enter the ID of the user you want to make an admin: ")
db.execute("UPDATE users SET admin = true WHERE id = ?", (id,))
db.commit()
print("Done!")
