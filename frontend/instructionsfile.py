

#this file simply stores strings needed
def get_ins(url):
    b = f'''
    INSTRUCTIONS
    1.Click on the desired epi no
    2.After that enable the website
    3.click on copy url and paste in 
      ur browser
    4.otherwise scan the url to connect
      with mobile phone
    5.available for devices in the wifi network
    the url is 
    
    {url}'''
    return b


def flaskappcode():
    return '''
import time
from flask import Flask,render_template

import threading
app=Flask(__name__,template_folder="animehtml")
import socket
c=0
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
@app.route("/anime")
def anime():
    return render_template("anime.html")

def k():
    time.sleep(3)
    import os
    os.kill(os.getpid(), 9)

@app.route("/shut")
def shut():
    threading.Thread(target=k).start()
    return ""
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=9000,debug=True,host=IPAddr)
    '''


def get_self():
    return '''
Hi User, This is an app developed for watching anime without
ads. Now about my self. My name is Jidu Krishna P J, and I'm
studying in 12th grade in CVV. This app is built with a mixture
of python concepts such as tkinter for frontend,fastapi for REST backend,
webscraping for collecting datas,threading for downloading thumbnails
for animes,flask for hosting websites,pickle for storing credentials,
keyring for storing user session ids,sqlite for storing user data and
at the same time managing its CRUD operations as well, css and html
custom-made for pc and devices with smaller screen such as mobile
to make it more user-friendly. The backend api is accessible via
https://api.jiduk.me/docs whenever it's online. Clients can access
it via session ids by coping it from down there. In short, it works by
validating the session key from the keyring and then making api calls.'''
