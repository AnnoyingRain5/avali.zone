import sqlite3

db = sqlite3.connect(
    "db/db.db", detect_types=sqlite3.PARSE_DECLTYPES
)

name = input("please enter the name of the category: ")
order = input("please enter the order of the category: ")
type = input("please enter the type of the category: ")

db.execute("INSERT INTO categories (name, displayorder, type) VALUES (?, ?, ?);", (name, order, type))
db.commit()
print("Done!")