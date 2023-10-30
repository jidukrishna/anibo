import os,sys,subprocess

f=["python -m pip install virtualenv & cd frontend & virtualenv venv & cd venv/scripts & activate & cd .. & cd .. & pip install -r requirements.txt",
    "python -m pip install virtualenv & cd backend & virtualenv venv & cd venv/scripts & activate & cd .. & cd .. & pip install -r requirements.txt"]

for i in f:
    subprocess.Popen(i,shell=True)
