import pickle
import os
import hashlib
import instructionsfile
import keyring
import requests

folders = ["/animehtml", "/acc"]
files = ["/animehtml/anime.html", "/acc/creds.pkl", "/history.csv", "/last_watched.pkl"]


# creates needed files and folder and returns the path
def runme():
    curr = os.path.join(os.path.expandvars("%APPDATA%"), "animanga")
    if os.path.exists(curr) and os.path.exists(curr + "/creditionals.pkl") and os.path.exists(curr + "/animehtml"):
        pass
    else:
        for i in folders:
            if os.path.exists(curr + i) == False:
                os.makedirs(curr + i)
        for i in files:
            if os.path.exists(curr + i) == False:
                with open(curr + i, "w"): pass
    if os.path.exists(curr + "/flaskappanime.py") == False:
        with open(curr + "/flaskappanime.py", "w") as f:
            f.write(instructionsfile.flaskappcode())

    if os.path.exists(curr + "/jidubhai.ico") == False:
        r = requests.get("https://raw.githubusercontent.com/jidukrishna/mangadownload/main/jidubhai.ico")
        with open(curr + "/jidubhai.ico", "wb") as f:
            f.write(r.content)
    return curr


# make a new user with session token
def create(email: str, session):
    dir_run = runme() + "/acc/creds.pkl"
    userhash = hashlib.sha256(email.encode()).hexdigest()
    with open(dir_run, "wb") as f: pickle.dump({email: userhash[::2]}, f)
    keyring.set_password("animanga", userhash[::2], session)


# gets the session id
def confirm():
    dir_run = runme() + "/acc/creds.pkl"
    with open(dir_run, "rb") as f:
        try:
            a = list(pickle.load(f).values())[0]
        except:
            return ""
        session = keyring.get_password("animanga", a)
        if session == None:
            return ""
        return session


# gets user mail
def get_mail():
    dir_run = runme() + "/acc/creds.pkl"
    with open(dir_run, "rb") as f:
        try:
            a = (pickle.load(f))
        except:
            return False
        mail = list(a.keys())[0]
        return mail


# deletes user when sign-out/delete
def delete():
    mail = get_mail()
    try:
        mail = hashlib.sha256(mail.encode()).hexdigest()
        keyring.delete_password("animanga", mail[::2])
    except:
        pass
    with open(runme() + "/acc/creds.pkl", "wb") as f:
        pass
    with open(runme() + "/last_watched.pkl", "w"):
        pass


# stores last watched
def get_last_watched():
    with open(runme() + "/last_watched.pkl", "rb") as f:
        try:
            a = pickle.load(f)
        except:
            return []
        if type(a) != list:
            return []
        else:
            return a


# adds last watched
def add_last_watched(name, epi_link):
    with open(runme() + "/last_watched.pkl", "wb") as f:
        pickle.dump([name, epi_link], f)
        return True
