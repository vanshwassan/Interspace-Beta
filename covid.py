import urllib.request as request
import json

with request.urlopen('http://localhost:5000/api/v1/get') as response:
    source = response.read()
    data = json.loads(source)


myfile = open("usernames.txt","r")
username = myfile.read()
Tester = username

def Check_Covid():
    if Tester == 