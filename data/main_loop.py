import multiprocessing
import screen_ocr
import requests
from data.config import *
from ahk import AHK
from data import window
import datetime


running = False
initialiazed = False
main_process = None
last_user = "" 

ahk = AHK()
def main_loop():
    ocr_reader = screen_ocr.Reader.create_reader(backend="easyocr")
    while True:
        ahk.send("/")
        results = ocr_reader.read_screen(bounding_box=(16, 303, 778, 375))
        parse(results.as_string())
        ahk.send("{BS}")
        ahk.send("{BS}")

def parse(result):
    try:
        result = result[result.find("["):]
        result = result.replace("[Global]: ", "")
        split = result.split("HAS FOUND")
        split[0] = split[0].strip()
        split[1] = split[1].strip()
        global last_user
        if split[0] == last_user:
            return
        else:
            last_user = split[0]
        for aura in globals:
            if aura["check"] in split[1].lower():
                send_stats(split[0], aura["name"], aura["rarity"])
                break
    except:
        print("fail")

def send_stats(username, aura_name, roll_chance):
    data = {
        "username" : "Genesis Stats Tracker"
    }
  
    data["embeds"] = [
        {
            "description" : "1 in " + roll_chance + "\n\nTime Discovered\n<t:" + str(int(datetime.datetime.now().timestamp())) + ":f>",
            "author" : {
                "name": username
            },
            "title": username + " has found " + aura_name
        }
    ]

    try:
        result = requests.post(webhook_url, json = data)
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    except:
        print("send error")
    else:
        pass

def start():
    global main_process
    global running
    if running == True:
        return
    else:
        running = True
        
    if window.focus_roblox() == -1:
        print("NO ROBLOX")
    
    main_process = multiprocessing.Process(target=main_loop)
    main_process.start()


def stop():
    global running
    if running == True:
        running = False
    else:
        return
    global main_process
    main_process.terminate()
