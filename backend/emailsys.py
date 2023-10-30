import smtplib
from random import randrange
import time
import sqlite3
import threading
import hashlib
import string
import random
from fastapi import HTTPException

# start the smtp port for emails
s = smtplib.SMTP('smtp.office365.com', 587)
s.starttls()
email_id_smtp="aniboexe@outlook.com"
password_smtp="Jidu@123"
s.login(user=email_id_smtp, password=password_smtp)

# create tables and databases
with sqlite3.connect('user.db', check_same_thread=False) as db:
    db.execute("create table if not exists user (email text,password text)")
    db.execute("create table if not exists token(email text,sess text)")

with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
    cur = db.cursor()
    cur.execute("create table if not exists pass_reset(email text,otp integer,time float)")
    cur.execute("create table if not exists delete_acc(email text,otp integer,time float)")
    cur.execute("create table if not exists signup_req(email text,password text,otp integer,time float)")

# email formats
formats = {

    "signup": {
        "title": "OTP FOR SIGN UP",
        "desc": "your signup otp which is valid for 6 min is\n\n\n"
    },

    "reset": {
        "title": "OTP FOR RESET",
        "desc": "your reset otp which is valid for 6 min is\n\n\n"
    },
    "delete": {
        "title": "OTP FOR DELETE",
        "desc": "your delete otp which is valid for 6 min is\n\n\n"
    }
}

# total contains str with chars for tokens
sp = "@#-"
total = string.printable[:62] + sp

# add new token to a email
def tokenadd(email: str):

    # generates tokens
    def get_token():
        token = "".join(random.choices(total, k=32))
        return token

    #manages token and adds it into the user db
    with sqlite3.connect('user.db', check_same_thread=False) as db:
        cur = db.cursor()
        while True:
            token = get_token()
            cur.execute("select * from token where sess=(?)", (token,))
            if len(cur.fetchall()) == 0:
                cur.execute("select * from token where email=?", (email,))
                if len(cur.fetchall()) == 0:
                    cur.execute("insert into token values(?,?)", (email, token))
                else:
                    cur.execute("update token set sess=? where email=?", (token, email))
                break
            else:
                pass
        return token

# validates a token
def validator(session):
    if session == "None": return False
    with sqlite3.connect('user.db', check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute("select * from token where sess=?", (session,))
        if len(cur.fetchall()) == 0:
            return False
        else:
            return True

# func for sending mail
def sendemail(a, email, typemail):
    format = formats[typemail]
    mes = f''' 
    {format["desc"]}
    OTP

        -----{a}----'''
    ti = f'{format["title"]}'
    message = 'Subject: {}\n\n{}'.format(ti, mes)
    message = str(message)
    s.sendmail(from_addr=email_id_smtp, to_addrs=email, msg=message)

# func for reseting . user will be checked and otp will be sent
def forgot_first_step(email: str, table_needed="pass_reset", meesg="reset"):
    with sqlite3.connect("user.db", check_same_thread=False) as db1:
        cur1 = db1.cursor()
        cur1.execute("select * from user where email=?", (email,))
        exists = cur1.fetchall()
    if len(exists) == 0:
        return HTTPException(status_code=404, detail="user not found")
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"delete from {table_needed} where email=?", (email,))
    a = randrange(100_000, 999_999)
    mailthread = threading.Thread(target=sendemail, args=(a, email, meesg))
    mailthread.start()
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"insert into {table_needed}(email,otp,time) values (?,?,?)", (email, int(a), time.time()))
    db.commit()
    mailthread.join()

    return {"status": "mssg send", }

# otp checked and user's password will be changed
def check_and_change(email: str, otp: int, password: str):
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"select * from pass_reset where email=?", (email,))
        data = cur.fetchall()
        if len(data) == 0:
            return HTTPException(status_code=404, detail="user not found")
        data = data[0]
        try:
            if time.time() - int(data[2]) < 600:
                if data[1] == otp:
                    with sqlite3.connect("user.db", check_same_thread=False) as db1:
                        cur1 = db1.cursor()
                        password = hashlib.sha256(password.encode()).hexdigest()
                        cur1.execute(f"update user set password=? where email=?", (password, email))
                        cur.execute(f"delete from pass_reset where email=?", (email,))
                    tk = tokenadd(email)
                    return {"status": "password reseted", "session": tk}
                else:
                    return HTTPException(status_code=401, detail="bad otp")

            else:
                cur.execute(f"delete from pass_reset where email=?", (email,))
                return HTTPException(status_code=410, detail="otp time over")
        except Exception as e:
            return HTTPException(status_code=410, detail="otp time over")


# otp checked and user deleted
def check_and_delete(email: str, otp: int):
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"select * from delete_acc where email=?", (email,))
        data = cur.fetchall()
        if len(data) == 0:
            return HTTPException(status_code=404, detail="user not found in queue")
        data = data[0]
        try:
            if time.time() - int(data[2]) < 600:
                if data[1] == otp:
                    with sqlite3.connect("user.db", check_same_thread=False) as db1:
                        cur1 = db1.cursor()
                        cur1.execute(f" delete from user where email=?", (email,))
                        cur.execute(f'delete from delete_acc where email=?', (email,))
                        cur1.execute("delete from token where email=?", (email,))
                    return {"status": "user deleted"}
                else:
                    return HTTPException(status_code=401, detail="bad otp")
            else:
                cur.execute(f'delete from delete_acc where email=?', (email,))
                return HTTPException(status_code=410, detail="otp time over")
        except Exception as e:
            return HTTPException(status_code=410, detail=f"otp time over {e}")


# signup with email,password and otp will be sent
def signup_req(email: str, password: str):
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"delete from signup_req where email=?", (email,))
    a = randrange(100_000, 999_999)
    mailthread = threading.Thread(target=sendemail, args=(a, email, "signup"))
    mailthread.start()
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute(f"insert into signup_req(email,password,otp,time) values (?,?,?,?)",
                    (email, password, int(a), time.time()))
    db.commit()
    mailthread.join()
    return {"status": "mssg send"}



# completes signup with otp validation
def signup(email: str, otp: int):
    with sqlite3.connect("acc_modifications.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(f"select * from signup_req where email=?", (email,))
        data = cur.fetchall()
        if len(data) == 0:
            return HTTPException(status_code=404, detail="user not found in queue")
        data = data[0]
        try:
            if time.time() - int(data[3]) < 600:
                if data[2] == otp:
                    with sqlite3.connect("user.db", check_same_thread=False) as db1:
                        cur1 = db1.cursor()
                        cur1.execute(f" insert into user values( ?,?)", (email, data[1]))
                        cur.execute(f"delete from signup_req where email=?", (email,))
                        db.commit()
                        db1.commit()
                    tk = tokenadd(email)
                    return {"status": "user created", "session": tk}
                else:
                    return HTTPException(status_code=401, detail="bad otp")
            else:
                cur.execute(f"delete from signup_req where email=?", (email,))
                return HTTPException(status_code=410, detail="otp time over")
        except Exception as e:
            return HTTPException(status_code=410, detail="otp time over")
