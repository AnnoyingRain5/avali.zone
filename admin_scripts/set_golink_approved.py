import sqlite3

db = sqlite3.connect(
    "db.db", detect_types=sqlite3.PARSE_DECLTYPES
)

id = input("please enter the ID of the user you want to approve for golinks: ")
db.execute("UPDATE users SET golink_approved = true WHERE id = ?", (id,))
db.commit()
print("Done!")