import instructionsfile
from info_dev2 import *
import keyringstorage
from arrange import word_fixer

request_url = "https://api.jiduk.me/"
session = keyringstorage.confirm()

headers = {"session": session}

headers_url = {"url": request_url, "session": headers}


def update_headers():
    global session, headers, headers_url
    session = keyringstorage.confirm()

    headers = {"session": session}

    headers_url = {"url": request_url, "session": headers}


hover_color = "#1ea61e"


# switch between main win and login/signup
def back():
    login_signup(main)
    main.withdraw()


# dev info tab view
class dev_info(c.CTkFrame):
    def __init__(self, win, root):

        super().__init__(win, width=1100, height=70, fg_color="#1e2021")
        update_headers()
        global main
        main = root

        def refe():
            update_headers()
            sessionkey = keyringstorage.confirm()
            sesssion_lab.configure(state="normal")
            sesssion_lab.delete("0.0", "end")
            sesssion_lab.insert("0.0", text="sessionkey  :  " + sessionkey)
            sesssion_lab.configure(state="disabled")

        def signout():
            update_headers()
            r = requests.post(f"{request_url}signout", headers=headers)
            try:
                if r.json()["status_code"] != 200:
                    messagebox.showinfo(message=r.json()["detail"])
                    return
            except:
                pass
            messagebox.showinfo(message=str(r.json()["status"]))
            keyringstorage.create(keyringstorage.get_mail(), "None")
            back()

        sessionkey = keyringstorage.confirm()
        print(sessionkey)
        lab = c.CTkLabel(self, text="::::About Myself:::::")
        lab.pack(pady=(10, 5))
        sesssion_lab = c.CTkTextbox(self, width=440, height=50)
        myself = c.CTkTextbox(self, width=600, height=300)
        myself.pack(pady=(10, 5))
        data = instructionsfile.get_self()
        myself.insert("0.0", text=word_fixer(data.replace("\n", " "), 600))
        myself.configure(state="disabled")
        sesssion_lab.insert("0.0", text="sessionkey  :  " + sessionkey)
        sesssion_lab.pack(pady=5)
        sesssion_lab.configure(state="disabled")
        refresh = c.CTkButton(self, text="refresh", command=refe, fg_color="green", hover_color=hover_color)
        refresh.pack(pady=5)
        signout = c.CTkButton(self, text="signout", command=signout, fg_color="green", hover_color=hover_color)
        signout.pack(pady=5)
        signout = c.CTkButton(self, text="delete/change pass", command=lambda: reset_delete(self, root),
                              fg_color="green"
                              , hover_color=hover_color)
        signout.pack(pady=5)

        self.pack(pady=(30, 0))
