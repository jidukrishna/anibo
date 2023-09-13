from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import uvicorn
import password_valid
import emailsys
import animehtml
import animedetails
import sqlite3
import hashlib

app = FastAPI()

# base url
gogo = "https://gogoanimehd.io/"


# validate the session header
def validate(session: str = Header(None)):
    return [emailsys.validator(session), session]


# models for params
class user(BaseModel):
    email: str
    password: str


class reset_password_struct(BaseModel):
    email: str
    otp: int
    new_password: str


class email_otp(BaseModel):
    email: str
    otp: int


class mail(BaseModel):
    email: str


class anime_link(BaseModel):
    link: str


# base entry point
@app.get("/")
async def welcome():
    return "official api for jidu anime app visit api.jiduk.me/docs for more"


# login endpoint
@app.post('/login/')
async def login(email_pass: user):
    # logs the user in and returns the session key
    # returns appropriate status code if anything else comes up
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (email_pass.email,))
        data = c.fetchall()
        if len(data) == 0:
            return HTTPException(status_code=404, detail="user not found")
        else:
            password = hashlib.sha256(email_pass.password.encode()).hexdigest()
            c.execute(f"select * from user where email=? and password=?", (email_pass.email, password))
            data = c.fetchall()
            if len(data) == 0:
                return HTTPException(status_code=401, detail="bad password")
            else:
                tk = emailsys.tokenadd(email_pass.email)
                return {'status': 'success', "session": tk}


# endpoint for signout and clears session id
# returns appropriate status code if anything else comes up

@app.post('/signout/')
async def login(session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=404, detail="user not logged in or doesnt exists")
    with sqlite3.connect('user.db', check_same_thread=False) as c:
        cur = c.cursor()
        cur.execute(f"update token set sess = 'None' where sess=?", (session[1],))
        return {"status": "signed out"}


# endpoint for signup email,password
# returns appropriate status code if anything else comes up

@app.post('/signup/')
async def register(user_signup: user):
    status_mail = password_valid.emailvalidity(user_signup.email)
    status = password_valid.passwordvalid(user_signup.password)
    if status_mail == False and status != "ok":
        return HTTPException(status_code=422, detail=f"not valid email and password {status}")
    if status_mail == False and status == "ok":
        return HTTPException(status_code=422, detail="not valid mail")

    if status_mail:
        with (sqlite3.connect('user.db', check_same_thread=False)) as c:
            c = c.cursor()
            c.execute(f"select * from user where email=?", (user_signup.email,))
            a = c.fetchall()
            if len(a) == 0:
                if status != True:
                    return {"status": status}
                k = emailsys.signup_req(user_signup.email, user_signup.password)
                return k
            else:
                return HTTPException(status_code=409, detail="user already exists")


# endpoint for signup completion email,otp
# returns appropriate status code if anything else comes up

@app.post("/signup/request")
async def register(user_signup_otp: email_otp):
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (user_signup_otp.email,))
        a = c.fetchall()
        if len(a) == 0:
            k = emailsys.signup(user_signup_otp.email, user_signup_otp.otp)
            return k

        else:
            return HTTPException(status_code=409, detail="user already exists")


# sends otp to reset password
# returns appropriate status code if anything else comes up

@app.put('/forgot/')
async def register(email: mail):
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (email.email,))
        a = c.fetchall()
        if len(a) == 0:
            return HTTPException(status_code=404, detail="user not found")
        else:
            status = emailsys.forgot_first_step(email.email)
            return status


# resets password based on validity of otp
# returns appropriate status code if anything else comes up

@app.put("/reset")
async def reset_password(reset_auto: reset_password_struct):
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (reset_auto.email,))
        a = c.fetchall()
        if len(a) == 0:
            return HTTPException(status_code=404, detail="user not found")
        else:
            data = password_valid.passwordvalid(reset_auto.new_password)
            if data != True:
                return HTTPException(status_code=422, detail=data)
            status = emailsys.check_and_change(reset_auto.email, reset_auto.otp, reset_auto.new_password)
            return status


# delete requests and otp will be sent
# returns appropriate status code if anything else comes up

@app.put("/delete/")
async def delete(user_delete: user):
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (user_delete.email,))
        data = c.fetchall()
        if len(data) == 0:
            return HTTPException(status_code=404, detail="user not found")
        else:
            password = hashlib.sha256(user_delete.password.encode()).hexdigest()

            c.execute(f"select * from user where email=? and password=?", (user_delete.email, password))
            data = c.fetchall()
            if len(data) == 0:
                return HTTPException(status_code=401, detail="bad password")
            else:
                status = emailsys.forgot_first_step(user_delete.email, table_needed="delete_acc", meesg="delete")
                return status


# delete if otp and mail is crrt
# returns appropriate status code if anything else comes up
@app.delete("/delete/request")
async def delete_user_data(del_user: email_otp):
    with (sqlite3.connect('user.db', check_same_thread=False)) as c:
        c = c.cursor()
        c.execute(f"select * from user where email=?", (del_user.email,))
        a = c.fetchall()
        if len(a) == 0:
            return HTTPException(status_code=404, detail="user not found")
        else:
            status = emailsys.check_and_delete(del_user.email, del_user.otp)
            return status


# validates and return anime search result
# returns appropriate status code if anything else comes up

@app.get("/anime")
async def results(search: str, session: str = Depends(validate)):
    if session[0] == False: return HTTPException(status_code=401, detail="invalid session")
    k = search
    b = animedetails.anime_search(k)
    if len(b) == 0:
        return HTTPException(status_code=403, detail="nah man its not available")
    else:
        return {"value": b}


# validates and return anime info
# returns appropriate status code if anything else comes up
@app.get("/anime/info")
async def results(link: str, session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=401, detail="invalid session")
    b = animedetails.anime_info(link)
    if len(b) == 0:
        return HTTPException(status_code=403, detail="idk ask the developer abt it")
    else:
        return {"value": b}


# validates and return anime epi link,download,comments
# not used in anibo but its for developer to put in their website
# returns appropriate status code if anything else comes up

@app.get("/anime-epi/watch")
async def anime_epi(link: str, epi: int, session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=401, detail="invalid session")

    link = gogo + link.split("/")[-1] + f"-episode-{epi}"
    try:
        data = animedetails.anime_epi_link(link)
        return {"value": data}
    except:
        return HTTPException(status_code=403, detail="idk ask the developer abt it")


# website test

@app.get("/test")
async def test():
    return {"status": "yes sir"}


# validates and return anime home pg list
# returns appropriate status code if anything else comes up

@app.get("/anime/home")
async def results(session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=401, detail="invalid session")
    b = animedetails.anime_home()
    if len(b) == 0:
        return HTTPException(status_code=403, detail="idk ask the developer abt it home")
    else:
        return {"value": b}


# validates and return anime html str
# returns appropriate status code if anything else comes up

@app.get("/anime/html")
async def anime_html(link: str, epi_no: str, img_src: str, info: str, session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=401, detail="invalid session")

    link = gogo + link.split("/")[-1] + f"-episode-{epi_no}"
    try:
        data = animehtml.anime_html_gene(link, str(epi_no), img_src, info)
    except:
        data = "None"
    if data == "None":
        return HTTPException(status_code=403, detail="idk ask the developer abt it")
    return {"value": data}


# gets current gogo link

@app.get("/gogo_current")
async def current_link():
    return gogo


# validates and return bool

@app.get("/anime/validate")
async def current_link(session: str = Depends(validate)):
    if session[0]:
        return {"status": True}
    else:
        return {"status": False}


# validates and return anime trending
# returns appropriate status code if anything else comes up

@app.get("/anime/trending")
async def results(kind: str = "", session: str = Depends(validate)):
    if not session[0]: return HTTPException(status_code=401, detail="invalid session")
    b = animedetails.getanimelist(kind)
    if len(b) == 0:
        return HTTPException(status_code=403, detail="it seems that myanimelist website is not working")
    else:
        return {"value": b}


# start the server running at localhost:8000
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
