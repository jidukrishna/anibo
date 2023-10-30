import csv
import os
import subprocess
import datetime
import animehtml
from uitrending import *
from io import BytesIO
from info_dev import *

control_sign_anime = 0
from sys import exit

# checks requirements
try:
    CREATE_NO_WINDOW = 0x08000000
    a = subprocess.check_output("python -V", creationflags=CREATE_NO_WINDOW)
    if not (int(str(a).split()[1].split(".")[0]) == 3 and int(str(a).split()[1].split(".")[1]) > 5):
        messagebox.showinfo(message="plz update or install python\nfrom "
                                    "microsoft store and add it to path\n"
                                    "environment variables\ncheck geeksforgeeks "
                                    "for easy process")
        exit()
    else:
        pass
except Exception as e:
    print(e)
    messagebox.showinfo(message="plz update or install python"
                                "\nfrom microsoft store and add it to path\n"
                                "environment variables\n"
                                "check geeksforgeeks for easy process")
    exit()

# install flask
try:
    subprocess.Popen("python -m pip", creationflags=CREATE_NO_WINDOW)
    subprocess.run(["python", "-m", "pip", "install", "Flask"], creationflags=CREATE_NO_WINDOW)
except subprocess.CalledProcessError as e:
    messagebox.showwarning(message=f"plz install and do \npip install Flask in \nglobal python interpreter {e.output}")
    exit()

# get wrkdir
wkdir = keyringstorage.runme()
os.chdir(wkdir)

hover_color = "#1ea61e"

ipv4 = socket.gethostbyname(socket.gethostname())
request_url = "http://127.0.0.1:8000/"

current_epi_anime = "nothing is playing as of now"
last_epi = None

# get last watched
try:
    last_from_pickle = keyringstorage.get_last_watched()
    current_epi_anime = last_from_pickle[0]
    last_epi = last_from_pickle[1]


except:
    current_epi_anime = "nothing is playing as of now"
    last_epi = None

flask_on_off = 0
home = 0
# get qrcode for localhost address flask
r_for_qr = requests.get(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=http://{ipv4}:9000/anime")
img_local = Image.open(BytesIO(r_for_qr.content))
img_local = c.CTkImage(img_local, size=(250, 250))

watchingrightnow = []

session = keyringstorage.confirm()

print(session)
headers = {"session": session}

headers_url = {"url": request_url, "session": headers}


def update_headers():
    global session, headers, headers_url
    session = keyringstorage.confirm()

    headers = {"session": session}

    headers_url = {"url": request_url, "session": headers}


# timing wrapper
def timing(func):
    def wrap(*args, **kwargs):
        a = time.time()
        func(*args, **kwargs)
        print(f"it took {func.__name__} : {time.time() - a}")

    return wrap

# switch between win signup/login
def change_to_login():
    login_signup(main_win)
    main_win.withdraw()


# check server working or not
def check_server():
    try:
        r = requests.get(f"{request_url}test")
        if r.json()["status"] != "yes sir":
            messagebox.showwarning(message=r.json()["status"])
            return False
        else:
            return True
    except:
        messagebox.showwarning(message="check your net or server not running")
        return False

c.set_appearance_mode("dark")

# main app class
class App(c.CTk):
    def __init__(self):
        super().__init__(fg_color="#131415")

        self.geometry("1228x688")
        self.title("Watch Anime")
        self.iconbitmap(default=keyringstorage.runme() + "/jidubhai.ico")
        global main_win
        main_win = self
        if not check_server(): return
        

        self.minsize(width=1100, height=688)

        # tab veiws for manga and anime etc
        tab_views = c.CTkTabview(self, width=1200, height=900, segmented_button_selected_color="green",
                                 fg_color="#131415",
                                 segmented_button_fg_color="#1e2021", segmented_button_selected_hover_color="green")
        tab_views.add("Anime")
        tab_views.add("Trending")
        tab_views.add("About Dev")
        anime(tab_views.tab("Anime"))
        animelistwin(tab_views.tab("Trending"), self)
        dev_info(tab_views.tab("About Dev"), self)

        tab_views.pack()

        # fetch gogourl
        global gogo
        update_headers()
        r = requests.get(f"{request_url}gogo_current", headers=headers)
        gogo = r.text.strip()

        # close the app and flask app
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

        self.mainloop()


# search / home /prev /web control buttons
@timing
class anime(c.CTkFrame):

    def __init__(self, root):
        super().__init__(root, fg_color="#131415")
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.rowconfigure((0,), weight=1)
        self.pack()

        if keyringstorage.confirm() == False:
            change_to_login()
            return

        # get last wathced above thing
        def last_viewed():
            if last_epi == None:
                messagebox.showinfo(message="no prev watched")
                return
            anime_epi_info(results_frame, last_epi)

        # control flask switch on and off
        @timing
        def flaas_main():
            def p():
                global flask_on_off, switch1
                if switch1.get() == 1:
                    control_flask.start(keyringstorage.runme())
                    flask_on_off = 1

                else:
                    control_flask.end(ipv4)
                    flask_on_off = 0
                if flask_on_off == 0:
                    switch.deselect(0)
                else:
                    switch.select(1)

            # flask frame
            fl_frame = c.CTkFrame(self, fg_color="#1e2021")
            fl_frame.grid(column=5, columnspan=3, row=1, padx=(40, 30), pady=3)
            global name_of_epi_label_main, switch1
            name_of_epi_label_main = c.CTkButton(fl_frame, text=current_epi_anime, command=last_viewed,
                                                 fg_color="green", hover_color=hover_color)
            name_of_epi_label_main.grid(row=0, column=0, columnspan=2, sticky="nsew")
            switch1 = c.CTkSwitch(fl_frame, command=p, text="WEBSITE", progress_color=("green"))
            switch1.grid(row=1, column=0)
            if flask_on_off == 0:
                switch1.deselect(0)
            else:
                switch1.select(1)

            def url_host():
                fl_frame.clipboard_clear()
                fl_frame.clipboard_append(f"http://{ipv4}:9000/anime")

            copy_url = c.CTkButton(fl_frame, text="copy url", command=url_host, width=100, fg_color="green",
                                   hover_color=hover_color)
            copy_url.grid(row=1, column=1, padx=(10, 0))

        def main_search_click():
            # anime search entry and submit
            global search_entry
            search_entry = c.CTkEntry(self, placeholder_text="type to search", width=150, height=35)
            search_entry.grid(column=1, row=1, columnspan=3, sticky="ew", padx=(20, 0))
            submit_search = c.CTkButton(self, text="search", command=lambda: search(search_entry.get()), width=100,
                                        corner_radius=7,
                                        fg_color="green", hover_color=hover_color)
            submit_search.grid(column=4, row=1, columnspan=1, padx=(10, 0))

            home_button = c.CTkButton(self, text="Home", command=lambda: search("i need home mister"), width=100,
                                      fg_color="green", hover_color=hover_color)
            home_button.grid(column=0, row=1)

        # load home screen
        def home():
            global home
            if home == 0:
                search("i need home mister")
                home += 1
            else:
                home += 1

        # search the words anime
        def search(words: str):
            update_headers()
            global control_sign_anime
            # remove all unnecessary
            global b
            if words == "i need home mister":
                # load home
                url = f"{request_url}anime/home"
            else:
                url = f"{request_url}anime?search={words.strip()}"

            b = []

            r = requests.get(url, headers=headers)
            try:
                if r.json()["status_code"] == 401:
                    if control_sign_anime != 0:
                        messagebox.showinfo(message=r.json()["detail"])
                    change_to_login()
                    return
                elif r.json()["status_code"] != 200:
                    messagebox.showinfo(message=r.json()["detail"])
                    return
            except:
                pass
            b = r.json()["value"]
            if b != "no-data":
                ko = 0
                # destroy prev results
                for i in root.winfo_children():
                    ko += 1
                    if ko > 1:
                        i.destroy()
                # display results from result class
                results(root)
            else:
                messagebox.showinfo(title="results", message="no result found")

        flaas_main()
        main_search_click()
        home()


# load the search res
@timing
class results(c.CTkScrollableFrame):

    def __init__(self, master, check=False):

        super().__init__(master, width=1200, height=900, fg_color="#1e2021")
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.pack()
        global results_frame
        results_frame = self
        update_headers()

        def anime_win(link):
            anime_epi_info(self, link)

        def load_search(i, j):
            if j == "toyota":
                # toyota for buttons without images
                img_button = c.CTkButton(self, command=lambda: anime_win(i[2]), text=i[0] + "\n reload to see the img",
                                         compound="top", fg_color="#131415",
                                         hover_color="grey")
                co_ord = i[3]
                img_button.grid(row=co_ord[0], column=co_ord[1], sticky="nwes", padx=7, pady=7, )
                return
            # for buttons with images

            img = Image.open(BytesIO(j))
            img = c.CTkImage(img, size=(180, 255))
            text = list(i[0])
            text.insert(10, "\n")
            img_button = c.CTkButton(self, image=img, command=lambda: anime_win(i[2]), text="".join(text),
                                     compound="top", fg_color="#131415",
                                     hover_color="grey", )

            co_ord = i[3]
            img_button.grid(row=co_ord[0], column=co_ord[1], sticky="news", padx=7, pady=7)

        # image_link_names_list_cord

        image_link_names_list_cord = arrange.main1(b)
        # destroy search results
        for i in self.winfo_children(): i.destroy()
        for i in image_link_names_list_cord:
            j = i[-1]
            if j is None:
                # for no image
                j = "toyota"
            load_search(i, j)


# show anime info
@timing
class anime_epi_info(c.CTkFrame):
    def __init__(self, master, link):
        super().__init__(master, width=1200, height=900, fg_color="#1e2021")
        self.pack_propagate(False)
        # get anime info

        data = {"link": link}
        update_headers()

        r = requests.get(f"{request_url}anime/info", params=data, headers=headers)

        try:
            if r.json()["status_code"] == 401:
                messagebox.showinfo(message=r.json()["detail"])
                change_to_login()
                return
            elif r.json()["status_code"] != 200:
                messagebox.showinfo(message=r.json()["detail"])
                return
        except:
            pass

        data = r.json()["value"]
        r = data
        heading = r[0]
        info = heading + '\n' + r[2]
        global epi_btn, clickedones
        clickedones = []
        epi_btn = []

        # frames
        def frames():
            # info used for showing info and  epi_scroll for epi buttons
            global infoframe, epi_scroll_frame
            infoframe = c.CTkFrame(self, height=280, width=475, fg_color="#1e2021")
            infoframe.pack_propagate(False)
            infoframe.grid(row=1, column=0, sticky="nsew")

            epi_scroll_frame = c.CTkScrollableFrame(self, width=700, fg_color="#131415")
            epi_scroll_frame.columnconfigure(9)
            epi_scroll_frame.grid(row=1, column=1, columnspan=1, sticky="nsew")

        # image label

        def image_label(epi=1):
            try:
                anime_img_frame = c.CTkFrame(self, fg_color="#1e2021")
                anime_img_frame.grid(row=0, column=0)
                anime_img = Image.open(BytesIO(requests.get(r[1], timeout=5).content))

                anime_img = c.CTkImage(anime_img, size=(180 * 1.5, 255 * 1.5))
                anime_img_label = c.CTkLabel(anime_img_frame, image=anime_img, text="")
                anime_img_label.grid(row=0, column=0)

                # added anime button



            except:
                messagebox.showwarning(title="no net", message="plz connect to network \n or retry")
                return

        # info
        def info_scroll():

            txtinfo = c.CTkTextbox(infoframe, width=350, height=300)
            txtinfo.insert("0.0", text=info.strip())
            txtinfo.configure(state="disabled")
            txtinfo.pack(fill="both")

        # make buttons
        def buttons_gen():

            button_arrange_values = arrange.buttons(r[-1])
            epi = 1
            for i in button_arrange_values:
                b1 = c.CTkButton(epi_scroll_frame, command=lambda epi=epi: anime_flask(info, r[1], epi, link),
                                 text=f'EPI {epi}',
                                 corner_radius=7, fg_color="#1f2224", hover_color="#159e37",
                                 border_color="black", border_width=2)
                b1.grid(row=i[0], column=i[1], sticky='nsew')
                epi_btn.append(b1)
                epi += 1
            try:
                if link.lstrip(gogo) == watchingrightnow[0]:
                    epi = watchingrightnow[1]
                    btn = epi_btn[epi - 1]
                    btn.configure(fg_color="#159e37")
            except Exception as e:
                print(e)

        # control flask app and set the heading and other things
        @timing
        def flaas():
            def p():
                global flask_on_off
                if switch.get() == 1:

                    control_flask.start(keyringstorage.runme())
                    print("on")

                    flask_on_off = 1

                else:
                    control_flask.end(ipv4)
                    flask_on_off = 0
                if flask_on_off == 0:
                    switch1.deselect(0)
                else:
                    switch1.select(1)

            fl_frame = c.CTkFrame(self, fg_color="#1e2021")
            fl_frame.grid(column=1, row=0, sticky="nsew")
            global name_of_epi_label, switch

            name_of_epi_label = c.CTkLabel(fl_frame, text=current_epi_anime)
            name_of_epi_label.grid(column=1, row=0, columnspan=1, sticky="nsew", pady=(0, 30))

            switch = c.CTkSwitch(fl_frame, command=p, text="WEBSITE", progress_color=("green"))
            switch.grid(column=1, row=2, padx=10)
            if flask_on_off == 0:
                switch.deselect(0)
            else:
                switch.select(1)

            def url_host():
                fl_frame.clipboard_clear()
                fl_frame.clipboard_append(f"http://{ipv4}:9000/anime")

            copy_url = c.CTkButton(fl_frame, text="copy url", command=url_host, width=120, fg_color="green",
                                   hover_color=hover_color)
            copy_url.grid(column=1, row=3, padx=(0, 0))

            # url for mobile devices
            url_label = c.CTkLabel(fl_frame, image=img_local, text="")
            url_label.grid(column=0, row=1, padx=10)
            instr_txt = c.CTkTextbox(fl_frame, width=400)
            import instructionsfile
            # fl_frame.columnconfigure(1,weight=1)
            instr_txt.insert("0.0", instructionsfile.get_ins(f"http://{ipv4}:9000/anime"))
            instr_txt.configure(state="disabled")
            instr_txt.grid(column=1, columnspan=2, row=1, sticky="nsew", padx=(13, 0))

        # abutton change color and load anime epi
        @timing
        def anime_flask(info, image, epi, link):
            print(epi)
            epi_btn[epi - 1].configure(fg_color="#159e37")
            global watchingrightnow
            try:
                print(watchingrightnow)
                if link.lstrip(gogo) == watchingrightnow[0]:
                    epiprev = watchingrightnow[1]
                    print(epiprev)
                    btn = epi_btn[epiprev - 1]
                    btn.configure(fg_color="#1f2224")
            except:
                pass

            update_headers()
            data = animehtml.get_anime_html(headers_url, link, epi, image, info)
            if data == "None" or data is None:
                messagebox.showwarning(message="no data available")
            else:

                with open(keyringstorage.runme() + "/animehtml/anime.html", "w", encoding="utf8") as f:
                    f.write(str(data))
                global current_epi_anime
                current_epi_anime = 'CURRENTLY PLAYING IN WEB:\n' + heading + 'EPI:' + str(epi)
                current_epi_anime1 = heading + ' epi:' + str(epi)
                name_of_epi_label.configure(text=current_epi_anime)
                name_of_epi_label_main.configure(text=current_epi_anime1)

                watchingrightnow = (link.lstrip(gogo), epi)
                global last_epi
                last_epi = link
                keyringstorage.add_last_watched(current_epi_anime1, last_epi)
                with open(keyringstorage.runme() + "/history.csv", "a", newline="") as f:
                    k = csv.writer(f)
                    if f.tell() == 0:
                        k.writerow(["anime", "epi", "date of watching", "link", "email"])
                    k.writerow([heading, epi, str(datetime.date.today()), link, keyringstorage.get_mail()])

        self.grid(row=0, column=0, rowspan=2, columnspan=6, sticky="nsew")

        frames()
        image_label()
        info_scroll()
        buttons_gen()
        flaas()


App()
