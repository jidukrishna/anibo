import schedule
import sqlite3
import time


# clears all pending timeover otp tables in acc_modification db
def cleanup():
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        a = time.time()
        cur = db.cursor()
        cur.execute("select tbl_name from sqlite_master")
        for i in cur.fetchall():
            print(i[0])
            cur.execute(f"delete from {i[0]} where {a}-time>600")


cleanup()
