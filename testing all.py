import uuid
def getUUID() :
    uuid_token = ""
    for i in range(3):
        uuid_token += str(uuid.uuid4())
    return uuid_token.strip()
print(getUUID())

from datetime import datetime
import time, os, requests
from termcolor import colored

os.system('color')
url = 'https://www.google.com/'
timeout = 2
sleep_time = 10
op = None

while True:
    now = datetime.now()
    try:
        op = requests.get(url, timeout=timeout).status_code
        if op == 200:
            print(now, colored("Connected", "green"))
            sleep_time = 10
        else:
            print(now, colored("Status Code is not 200", "red"))
            print("status Code", op)
    except:
        print(now, colored("Not Connected", "red"))
        print("status Code", op)
        sleep_time = 5
    time.sleep(sleep_time)
