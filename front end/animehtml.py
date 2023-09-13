from tkinter import messagebox

import requests


# get html file from backend
def get_anime_html(headersurl, link, epi_no, img_src="None", info="None"):
    params = {"epi_no": epi_no, "img_src": img_src, "info": info, "link": link}
    try:
        r = requests.get(f"{headersurl['url']}anime/html", params=params, headers=headersurl["session"])
        try:
            if r.json()["status_code"] != 200:
                messagebox.showinfo(message=r.json()["detail"])
                return
        except:
            pass
        data = r.json()

        return data["value"]
    except Exception as e:
        return None
