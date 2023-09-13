import threading
import subprocess
import requests

CREATE_NO_WINDOW = 0x08000000


def k(curr):
    subprocess.run(["python", curr + "/flaskappanime.py"], creationflags=CREATE_NO_WINDOW)


# start flask app in roaming dir with html file
def start(curr):
    global olo
    olo = threading.Thread(target=k, args=(curr,))
    olo.start()


# close the website
def end(ipv4):
    requests.get(f"http://{ipv4}:9000/shut")
    global olo
    olo.join()


if __name__ == "__main__":
    start("/animeproj")
