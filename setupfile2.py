import os,sys,subprocess



f=[r".\backend\venv\scripts\activate",r".\backend\main.py",r".\frontend\venv\scripts\activate",r".\frontend\ui1.py"]
c=0
for i in f:
    if c==0:
        print("starting server at http://127.0.0.1:8000/docs")
        c=1
    subprocess.Popen(i,shell=True)