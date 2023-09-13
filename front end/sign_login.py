import socket
import threading
import time
import requests
from tkinter import messagebox
import customtkinter as c
import validitychecker
from sys import exit
from sys import platform
import control_flask
import keyringstorage

visible = 0
username = "jidu"
passw = "123"
pass1show_login = 0
pass2show_login = 0
pass1show = 0
pass2show = 0
email_user = password_user = ""
email_user_reset = password_user_reset = ""

request_url = "http://127.0.0.1:8000"

ipv4 = socket.gethostbyname(socket.gethostname())
hover_color = "#1ea61e"

main_window = ""


# login signup window
class login_signup(c.CTkToplevel):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#131415")
        global main_window
        self.title("login/signup/forgot")
        self.iconbitmap(default=keyringstorage.runme() + "/jidubhai.ico")
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(keyringstorage.runme() + "/jidubhai.ico"))
        self.maxsize(width=750, height=450)
        self.minsize(width=750, height=450)
        main_window = master
        self.pack_propagate(False)
        self.geometry("750x450")

        def close():
            b = messagebox.askyesno(message="quit?")
            if b:
                try:
                    control_flask.end(ipv4)
                except:
                    pass
                exit()

            else:
                pass

        self.protocol("WM_DELETE_WINDOW", close)
        tabs = c.CTkTabview(self, height=300,
                            segmented_button_selected_color="green", fg_color="#131415",
                            segmented_button_fg_color="#1e2021", segmented_button_selected_hover_color="green")
        global login_signup_win
        login_signup_win = self
        tabs.place(rely=.5, relx=.5, anchor="center")
        tabs.add("login")
        tabs.add("sign up")
        tabs.add("forgot password")
        signup(tabs.tab("sign up"), height=300, width=700)
        login(tabs.tab("login"), height=300, width=700)
        forgot(tabs.tab("forgot password"), height=300, width=700)


# signup window
class signup(c.CTkFrame):
    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        self.pack_propagate(False)
        self.configure(fg_color="#1e2021")
        global signupwin
        signupwin = self

        def display(n):
            global pass1show, pass2show
            if n == 1:
                if pass1show == 0:
                    pass1show = 1
                    pass1_sign.configure(show="")
                    eye1.configure(text="U_U")
                else:
                    pass1show = 0
                    pass1_sign.configure(show="*")
                    eye1.configure(text="O_O")

            else:
                if pass2show == 0:
                    pass2show = 1
                    pass2.configure(show="")
                    eye2.configure(text="U_U")
                else:
                    pass2show = 0
                    pass2.configure(show="*")
                    eye2.configure(text="O_O")

        def check_bfr_proceeding():
            mail_value = email.get().strip()
            pass1_value = pass1_sign.get()
            pass2_value = pass2.get()
            mail_status = validitychecker.emailvalidity(mail_value)
            password_status = validitychecker.passwordvalid(pass1_value, pass2_value)
            if mail_status == False:
                messagebox.showinfo(message="enter valid email")
                return
            if password_status != True:
                messagebox.showinfo(message=password_status)
                return
            else:
                global email_user, password_user
                email_user = mail_value
                password_user = pass1_value
                data = {
                    "email": email_user,
                    "password": password_user
                }
                value = requests.post(f'{request_url}/signup', json=data)
                print(value.content)
                try:
                    if value.json()["status_code"] != 200:
                        messagebox.showinfo(message=value.json()["detail"])
                        return
                except:
                    pass
                if value.json()["status"]:
                    messagebox.showinfo(message="otp has been sent")
                    otpwindow(win)
                else:
                    messagebox.showinfo(message=str(value.json()["status"]))
                    return

        global pass1_sign, pass2
        c.CTkLabel(self, text="SIGNUP TODAY!!!").grid(column=0, columnspan=3, row=0, padx=(5), pady=(20, 0))

        email = c.CTkEntry(self, placeholder_text="email", height=35, width=245)
        email.grid(column=0, columnspan=3, row=1, padx=(5), pady=(20, 0))
        pass1_sign = c.CTkEntry(self, placeholder_text="password", show="*")
        pass1_sign.grid(column=0, columnspan=2, row=2, sticky="nsew", ipadx=40, padx=(5, 0), pady=10)
        eye1 = c.CTkButton(self, text="O_O", width=35, command=lambda: display(1), height=35, fg_color="green",
                           hover_color=hover_color)
        eye1.grid(column=2, row=2, sticky="ne", padx=(0, 5), pady=10)
        pass2 = c.CTkEntry(self, placeholder_text="re-enter password", show="*")
        pass2.grid(column=0, columnspan=2, row=3, sticky="nsew", padx=(5, 0), pady=(0, 10))
        eye2 = c.CTkButton(self, text="O_O", width=35, height=35, command=lambda: display(2), fg_color="green",
                           hover_color=hover_color)
        eye2.grid(column=2, row=3, sticky="ne", padx=(0, 5), pady=(0, 10))
        submit = c.CTkButton(self, text="submit", command=check_bfr_proceeding, fg_color="green",
                             hover_color=hover_color)
        submit.grid(column=0, columnspan=2, row=4, sticky="nsew", padx=(5), pady=(0, 10))
        self.place(rely=.5, relx=.5, anchor="center")


# signup otp window

class otpwindow(c.CTkFrame):
    print("yea")

    def __init__(self, win, **kwargs):
        signupwin.place_forget()
        super().__init__(win, **kwargs)
        self.configure(fg_color="#1e2021")
        self.pack_propagate(False)

        def back():
            self.destroy()
            signupwin.place(rely=.5, relx=.5, anchor="center")
            pass1_sign.delete(0, "end")
            pass2.delete(0, "end")

        def start():
            sec = 360
            count = 60
            for i in range(1, 361):
                time.sleep(1)
                total = sec - i
                min_lab = total // count
                sec_lab = total % count
                text_for_timer = f"0{min_lab}:{sec_lab}'s remaining"
                timer.configure(text=text_for_timer)
                if min_lab == 0 and sec_lab == 0:
                    text_for_timer = "time over"
                    timer.configure(text=text_for_timer)
                    back()
                    messagebox.showinfo(message="time over try again")
                    break

        def register_user():
            otp = otpentry.get()
            if otp.isdigit() == False:
                messagebox.showinfo(message="enter only digits")
                return
            if len(otp) != 6:
                messagebox.showinfo(message="otp has to be of 6 digits")
                return
            data = {
                "email": email_user,
                "otp": otp
            }
            value = requests.post(f"{request_url}/signup/request", json=data)
            try:
                if value.json()["status_code"] != 200:
                    messagebox.showinfo(message=value.json()["detail"])
                    return
            except:
                pass
            status = value.json()["status"]
            session = value.json()["session"]
            if status == "user created":
                messagebox.showinfo(message="successfully acc created")

                keyringstorage.create(email_user, session)

                login_signup_win.destroy()
                login_signup_win.update()
                main_window.deiconify()
                main_window.update()
            else:
                messagebox.showinfo(message=status)

        otp_mssg = c.CTkLabel(self, text=f"otp has been sent to:\n{email_user}")
        otp_mssg.place(rely=.09, relx=.5, anchor="center")

        timer = c.CTkLabel(self, text="06:00")
        timer.place(rely=.3, relx=.5, anchor="center")
        threading.Thread(target=start, daemon=True).start()

        otpentry = c.CTkEntry(self)
        otpentry.place(rely=.5, relx=.5, anchor="center")
        submit = c.CTkButton(self, text="submit", command=register_user, fg_color="green", hover_color=hover_color)
        submit.place(rely=.7, relx=.5, anchor="center")
        back_button = c.CTkButton(self, text="signup page", command=back, fg_color="green", hover_color=hover_color)
        back_button.place(rely=.85, relx=.5, anchor="center")
        self.place(rely=.5, relx=.5, anchor="center")


# login window
class login(c.CTkFrame):
    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        self.pack_propagate(False)
        self.configure(fg_color="#1e2021")

        def display():
            global pass1show_login
            if pass1show_login == 0:
                pass1show_login = 1
                pass1.configure(show="")
                eye1.configure(text="U_U")
            else:
                pass1show_login = 0
                pass1.configure(show="*")
                eye1.configure(text="O_O")

        def login_req():

            mail_value = email.get()
            pass1_value = pass1.get()
            mail_status = validitychecker.emailvalidity(mail_value)
            password_status = validitychecker.passwordvalid(pass1_value, pass1_value)
            if mail_status == False:
                messagebox.showinfo(message="enter valid email")
                return
            if password_status != True:
                messagebox.showinfo(message="bad password")
                return
            else:

                data = {
                    "email": mail_value,
                    "password": pass1_value
                }
                value = requests.post(f'{request_url}/login', json=data)
                try:
                    if value.json()["status_code"] != 200:
                        messagebox.showinfo(message=value.json()["detail"])
                        return
                except:
                    pass
                print(value.json())
                data = value.json()["status"]
                session = value.json()["session"]
                if data == "success":
                    messagebox.showinfo(message="success")
                    keyringstorage.create(mail_value, session)
                    login_signup_win.destroy()
                    main_window.deiconify()
                    main_window.update()

                else:
                    messagebox.showinfo(message=data)

        global pass1
        c.CTkLabel(self, text="WELCOME, USER!!!").grid(column=0, columnspan=3, row=0, padx=(5), pady=(20, 0))
        email = c.CTkEntry(self, placeholder_text="email", height=35, width=245)
        email.grid(column=0, columnspan=3, row=1, padx=(5), pady=(20, 0))
        pass1 = c.CTkEntry(self, placeholder_text="password", show="*")
        pass1.grid(column=0, columnspan=2, row=2, sticky="nsew", ipadx=40, padx=(5, 0), pady=10)
        eye1 = c.CTkButton(self, text="O_O", width=35, command=display, height=35, fg_color="green",
                           hover_color=hover_color)
        eye1.grid(column=2, row=2, sticky="ne", padx=(0, 5), pady=10)
        submit = c.CTkButton(self, text="submit", command=login_req, fg_color="green", hover_color=hover_color)
        submit.grid(column=0, columnspan=2, row=4, sticky="nsew", padx=(5), pady=(0, 10))
        self.place(rely=.5, relx=.5, anchor="center")


# boiler plate forgot window
class forgot(c.CTkFrame):
    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        self.pack_propagate(False)
        self.configure(fg_color="#1e2021")
        global forgot_win
        forgot_win = self

        def forgot_req():
            mail_value = email.get().strip()
            mail_status = validitychecker.emailvalidity(mail_value)
            print(mail_status)
            if mail_status:
                data = {"email": mail_value}
                response = requests.put(f"{request_url}/forgot", json=data)
                try:
                    if response.json()["status_code"] != 200:
                        messagebox.showinfo(message=response.json()["detail"])
                        return
                except:
                    pass
                status = response.json()["status"]
                if status == "mssg send":
                    global email_user_reset
                    email_user_reset = mail_value
                    messagebox.showinfo(message="otp has been sent")
                    forgototpwin(win)
                else:
                    messagebox.showinfo(message=status)
            else:
                messagebox.showinfo(message="enter valid email")

        info_forgot = "Hello user, inorder to reset ur password\nplz enter ur email and continue forward"
        explain = c.CTkLabel(self, text=info_forgot)
        explain.place(rely=.37, relx=.5, anchor="center")
        email = c.CTkEntry(self, placeholder_text="email", height=35, width=245)
        email.place(rely=.53, relx=.5, anchor="center")
        submit = c.CTkButton(self, text="submit", command=forgot_req, fg_color="green", hover_color=hover_color)
        submit.place(rely=.69, relx=.5, anchor="center")
        self.place(rely=.5, relx=.5, anchor="center")


# boiler plate forgot otp window
class forgototpwin(c.CTkFrame):
    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        forgot_win.place_forget()
        self.configure(fg_color="#1e2021")
        self.pack_propagate(False)

        def display(n):
            global pass1show, pass2show
            if n == 1:
                if pass1show == 0:
                    pass1show = 1
                    pass1.configure(show="")
                    eye1.configure(text="U_U")
                else:
                    pass1show = 0
                    pass1.configure(show="*")
                    eye1.configure(text="O_O")

            else:
                if pass2show == 0:
                    pass2show = 1
                    pass2.configure(show="")
                    eye2.configure(text="U_U")
                else:
                    pass2show = 0
                    pass2.configure(show="*")
                    eye2.configure(text="O_O")

        def check_bfr_proceeding():
            pass1_value_reset = pass1.get()
            pass2_value_reset = pass2.get()
            otp = otp_wid.get()
            if otp.isdigit() == False:
                messagebox.showinfo(message="enter valid otp")
                return
            if len(otp) != 6:
                messagebox.showinfo(message="otp has to be of 6 digits")
                return
            password_status = validitychecker.passwordvalid(pass1_value_reset, pass2_value_reset)

            if password_status != True:
                messagebox.showinfo(message=password_status)
                return
            else:
                data = {
                    "email": email_user_reset,
                    "otp": otp,
                    "new_password": pass1_value_reset
                }
                value = requests.put(f'{request_url}/reset', json=data)
                try:
                    if value.json()["status_code"] != 200:
                        messagebox.showinfo(message=value.json()["detail"])
                        return
                except:
                    pass
                if value.json()["status"] == "password reseted":
                    messagebox.showinfo(message="password changed successfully")
                    session = value.json()["session"]
                    keyringstorage.create(email_user_reset, session)
                    login_signup_win.destroy()
                    login_signup_win.update()
                    main_window.deiconify()
                    main_window.update()

                else:
                    messagebox.showinfo(message=str(value.json()["status"]))
                    return

        def back():
            self.destroy()
            forgot_win.place(rely=.5, relx=.5, anchor="center")

        def start():
            sec = 360
            count = 60
            for i in range(1, 361):
                time.sleep(1)
                total = sec - i
                min_lab = total // count
                sec_lab = total % count
                text_for_timer = f"0{min_lab}:{sec_lab}'s remaining"
                timer.configure(text=text_for_timer)
                if min_lab == 0 and sec_lab == 0:
                    text_for_timer = "time over"
                    timer.configure(text=text_for_timer)
                    back()
                    messagebox.showinfo(message="time over try again")
                    break

        global pass1, pass2
        timer = c.CTkLabel(self, text="06:00")
        timer.grid(column=1, row=0, columnspan=3, sticky="nsew", )
        threading.Thread(target=start, daemon=True).start()

        otp_wid = c.CTkEntry(self, placeholder_text="otp", height=35, width=245)
        otp_wid.grid(column=1, columnspan=3, row=1, padx=(5), pady=(0, 0))
        pass1 = c.CTkEntry(self, placeholder_text="password", show="*")
        pass1.grid(column=1, columnspan=2, row=2, sticky="nsew", ipadx=40, padx=(5, 0), pady=10)
        eye1 = c.CTkButton(self, text="O_O", width=35, command=lambda: display(1), height=35, fg_color="green",
                           hover_color=hover_color)
        eye1.grid(column=3, row=2, sticky="ne", padx=(0, 5), pady=10)
        pass2 = c.CTkEntry(self, placeholder_text="re-enter password", show="*")
        pass2.grid(column=1, columnspan=2, row=3, sticky="nsew", padx=(5, 0), pady=(0, 10))
        eye2 = c.CTkButton(self, text="O_O", width=35, height=35, command=lambda: display(2), fg_color="green",
                           hover_color=hover_color)
        eye2.grid(column=3, row=3, sticky="ne", padx=(0, 5), pady=(0, 10))
        submit = c.CTkButton(self, text="submit", command=check_bfr_proceeding, fg_color="green",
                             hover_color=hover_color)
        submit.grid(column=1, columnspan=2, row=4, sticky="nsew", padx=(5), pady=(0, 10))
        go_back = c.CTkButton(self, text="forgot pg", command=back, fg_color="green", hover_color=hover_color)
        go_back.grid(column=1, columnspan=2, row=5, sticky="nsew", padx=(5), pady=(0, 10))
        self.place(rely=.5, relx=.5, anchor="center")
