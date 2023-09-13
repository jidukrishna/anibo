import threading
import requests
from bs4 import BeautifulSoup

# base scrape url
main_url = "https://gogoanimehd.io/"


# word adjuster a=takes str and f=adjusts the line breaker
def word_fixer(a, f=70):
    b = ""
    for i in a.split("\n"):
        if len(i) < f:
            b += i + '\n'
        else:
            k = ""
            for j in i.split():
                k += j + " "
                if len(k) > f:
                    b += k + '\n'
                    k = ''
            if len(k) <= f:
                b += k + '\n'
    return b


# takes a search query and gives out list
# containing the results with imgs,heading ,links,etc
def anime_search(word):
    to_be_searched = word.strip()
    rep = requests.get(f"{main_url}/search.html?keyword={to_be_searched}")
    be = BeautifulSoup(rep.content, "lxml")
    f = be.find("ul", class_="items")
    items = f.find_all("li")
    b = []
    c = 0
    for i in items:
        try:
            tag_img = i.find("img")["src"]
            tag_name = i.find("p", class_="name")
            tag_link = main_url + i.find("a")["href"]
            release = i.find("p", class_="released")
            b.append((tag_name.text.strip() + f"\n{release.text.strip()}", tag_img, tag_link))
        except Exception as e:
            print(e)
        c += 1
        if c == 30:
            break

    # adds column and grid positions for tkinter
    if len(b) != 0:
        column = 0
        row = 2
        js = []
        for i in (b):
            if column == 6:
                column = 0
                row += 1
            js.append((*i, (row, column)))
            column += 1
        return js
    return b


# takes gogo link and scrapes anime info
def anime_info(link):
    r = requests.get(link).content
    b = BeautifulSoup(r, "lxml")
    main_info = b.find("div", class_="anime_info_body")
    image = main_info.find("img")["src"]
    heading = main_info.find("h1").text.strip()

    # p_tags collects the anime desc with heading

    p_tags = [i for i in main_info.find_all("p")[1:]]
    info = ''
    for i in p_tags:
        info += (i.text.strip()) + "\n"
    latest_tag = b.find("ul", {"id": "episode_page"})
    latest = latest_tag.find_all("a")[-1]
    latest = latest["ep_end"].strip()
    return heading, image, word_fixer(info), int(latest)


# finds the epi link --source from consumet api running
# locally on computer other info scraped. used threading
# since it's an io based task. comments scaped from the disqs thread
def anime_epi_link(link):
    video_link = ""
    video_b = []

    def consumet(link):
        global video_link
        url = f"http://127.0.0.1:3000/anime/gogoanime/watch/{link}"
        response = requests.get(url)
        data = response.json()
        video_link = data["sources"][-2]["url"]
        video_b.append(video_link)

    consumet_thread = threading.Thread(target=consumet, args=(link.split("/")[-1],))
    consumet_thread.start()
    r = requests.get(link).content
    b = BeautifulSoup(r, "lxml")
    f = b.find("li", class_="dowloads")
    link_to_download = f.find("a")["href"]
    disqs = b.find("div", class_="disq")
    consumet_thread.join()
    return video_b[0], link_to_download, str(disqs)


# boilerplate of anime search,but it gives the gogo anime
# home pg results
def anime_home():
    rep = requests.get(main_url)
    be = BeautifulSoup(rep.content, "lxml")
    f = be.find("ul", class_="items")
    items = f.find_all("li")
    b = []
    c = 0
    for i in items:
        try:
            tag_img = i.find("img")["src"]
            tag_name = i.find("p", class_="name")
            release = i.find("p", class_="episode")
            tag_link = main_url + '/category/' + "-".join(str(i.find("a")["href"]).split("-")[:-2])
            title = word_fixer(tag_name.text.strip(), 30).strip() + f"\n{release.text.strip()}"
            b.append((title.strip(), tag_img, tag_link))
        except Exception as e:
            print(e)
        c += 1
        if c == 30:
            break
    if len(b) != 0:
        column = 0
        row = 2
        js = []
        for i in b:
            if column == 6:
                column = 0
                row += 1
            js.append((*i, (row, column)))
            column += 1
        return js
    return b


# webscrapes from myanimelist for ranking of animes
# returns list with names,img,stars,ratings
def getanimelist(kind: str = ""):
    values = []
    r = requests.get(f"https://myanimelist.net/topanime.php?type={kind}")
    b = BeautifulSoup(r.content, "lxml")
    data = b.find_all("tr", class_="ranking-list")

    for i in data:
        data_of_anime = list(i.find_all("td"))
        img = data_of_anime[1].find("img")["data-srcset"].split(",")[1].rstrip("2x").strip()
        rank = data_of_anime[0].text.strip()
        heading = data_of_anime[1].text.strip().split("\n")[0]
        heading = "".join([i for i in heading if ord(i) < 128])
        info = "\n".join(data_of_anime[1].text.strip().split("\n")[1:4]).strip()
        stars = data_of_anime[2].text.strip()
        values.append([img, rank, heading, info, stars])
    return values
