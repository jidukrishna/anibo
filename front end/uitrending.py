from io import BytesIO
import arrange
from PIL import Image
from sign_login import *

# button keys dictionary
animelist = {"Top Anime Series": "", "Top Airing Anime": "airing", "Top Upcoming Anime": "upcoming",
             "Top Anime TV Series": "tv", "Top Anime by Popularity": "bypopularity",
             "Top Anime Movies": "movie", "Top Anime OVA Series": "ova", "Top Anime ONA Series": "ona",
             "Top Anime Specials": "special", "Top Favorited Anime": "favorite"}

session = keyringstorage.confirm()

headers = {"session": session}
request_url = "https://api.jiduk.me/"

headers_url = {"url": request_url, "session": headers}

control_sign = 0
hover_color = "#1ea61e"


def update_headers():
    global session, headers, headers_url
    if session == False:
        session = ""
    session = keyringstorage.confirm()

    headers = {"session": session}

    headers_url = {"url": request_url, "session": headers}


# decorator for timer
def timing(func):
    def wrap(*args, **kwargs):
        a = time.time()
        func(*args, **kwargs)
        print(f"it took {func.__name__} : {time.time() - a}")

    return wrap


# window switching
def change_to_login():
    login_signup(main_win)
    main_win.withdraw()


# trending buttons generation
@timing
class animelistwin(c.CTkFrame):
    def __init__(self, win, root):
        global main_win
        main_win = root
        super().__init__(win, fg_color="#1e2021", width=1100, height=70)

        def get_anime_list(i):
            k = 1
            for j in win.winfo_children():
                if k == 2:
                    j.destroy()
                k += 1
            res(win, animelist[i], i)

        buttons = ["Top Anime Series", "Top Airing Anime", "Top Upcoming Anime", "Top Anime TV Series",
                   "Top Anime by Popularity",
                   "Top Anime Movies", "Top Anime OVA Series", "Top Anime ONA Series", "Top Anime Specials",
                   "Top Favorited Anime"]
        col = row = 0
        for i in buttons:
            nah = c.CTkButton(self, text=i + "\u2606", command=lambda i=i: get_anime_list(i), fg_color="green",
                              hover_color=hover_color)

            nah.grid(column=col, row=row, sticky="nsew", pady=5, padx=5)
            col += 1
            if col == 5:
                col = 0
                row += 1

        self.pack(pady=(20, 0))
        res(win)

# show results when button clicked
@timing
class res(c.CTkScrollableFrame):
    def __init__(self, win, value="", check="Top Anime Series"):
        global control_sign

        super().__init__(win, width=750, height=600, fg_color="#1e2021")
        for i in self.winfo_children(): print(i)
        update_headers()
        r = requests.get(f"{headers_url['url']}anime/trending", headers=headers_url["session"], params={"kind": value})
        try:
            if r.json()["status_code"] == 401 and control_sign != 0:
                messagebox.showinfo(message=r.json()["detail"])
                change_to_login()
                return
            elif r.json()["status_code"] != 200:
                messagebox.showinfo(message=r.json()["detail"])
                return
        except:
            pass
        data = r.json()["value"]
        control_sign = 1
        if data == "no-data":
            messagebox.showinfo(message="server issue ig??")
            return
        data = arrange.main12(data)
        row = 1
        size = 2

        # just heading labels
        k = c.CTkFrame(self, width=800, corner_radius=25, fg_color="#131415")
        rank = c.CTkLabel(k, text="Rank", width=100, height=50)
        rank.grid(column=0, row=0, padx=40)

        heading = c.CTkLabel(k, text=check, height=50)
        heading.grid(column=1, row=0, padx=70)

        stars = c.CTkLabel(k, text="Rating" + "\u2b50", width=100, height=50)
        stars.grid(column=2, row=0, padx=4)

        k.grid(column=0, row=0, sticky="nsew", pady=10)

        for i in data:
            k = c.CTkFrame(self, width=900, height=100, corner_radius=25, fg_color="#131415")
            if type(i[0]) != bytes:
                imglabel = c.CTkLabel(k, text="plz load to see the img")
                imglabel.grid(column=3, row=0, rowspan=2, sticky="nsew", padx=10, pady=10)
            else:
                img = c.CTkImage(Image.open(BytesIO(i[0])), size=(50 * size, 70 * size))
                imglabel = c.CTkLabel(k, image=img, text="")
                imglabel.grid(column=3, row=0, rowspan=2, sticky="nsew", padx=10, pady=10)

            rating = c.CTkLabel(k, text=i[1], width=100, height=140, font=("Copperplate Gothic Bold", 22))
            rating.grid(column=0, row=0, rowspan=2, padx=40)

            heading = c.CTkLabel(k, text=i[2], wraplength=250)
            heading.grid(column=1, row=0, padx=40)

            infolabel = c.CTkLabel(k, text=i[3])
            infolabel.grid(column=1, row=1, sticky="nsew", padx=40, ipady=10)

            stars = c.CTkLabel(k, text=(i[4] + "\u2b50"), width=100, height=140)
            stars.grid(column=2, row=0, padx=40, rowspan=2)

            k.grid(column=0, row=row, sticky="nsew", pady=5)
            row += 1

        self.pack(pady=(15, 0))
