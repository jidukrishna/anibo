import re
import string

low = string.ascii_lowercase
up = string.ascii_uppercase
no = string.printable[:10]
sym = string.printable[62:]

# password validity checker same as that of backend
def passwordvalid(p1: str, p2: str):
    if p1 == "" or p2 == "": return "plz enter password 8 char long \n containing up,low,sym,digits"
    if p1[0] == " " or p1[-1] == " ":
        return "no spaces at beginning or ending"
    p1 = p1.strip()
    p2 = p2.strip()
    if p1 != p2:
        return "not same"
    else:
        password = p1
        short = upcon = lowcon = nocon = symcon = False
        if len(password) >= 8: short = True
        for i in password:
            if i in up: upcon = True
            if i in low: lowcon = True
            if i in no: nocon = True
            if i in sym: symcon = True
        if short and nocon and upcon and nocon and symcon and lowcon:
            return True
        else:
            text = "plz add"
            if short == False: text += " more than 8 char,"
            if nocon == False: text += " numbers,"
            if upcon == False: text += " uppercase,"
            if lowcon == False: text += " lowercase,"
            if symcon == False: text += " symbols,"
        return text.strip(",")

# email validity checker same as that of backend
def emailvalidity(mail):
    emailreg = re.compile(r"[a-zA-Z0-9.+_-]+@+[a-zA-Z0-9.-]+.+\.[a-zA-Z0-9.+_-]{2,7}$")
    m = re.match(emailreg, mail)
    if m:
        return True
    else:
        return False
