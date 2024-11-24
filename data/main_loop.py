import multiprocessing
import screen_ocr
import requests
from data.config import *
from ahk import AHK
import datetime
import sys

sys.dont_write_bytecode = True
running = False
initialiazed = False
main_process = None
last_user = "" 

ahk = AHK()
def main_loop():
    counter = 0
    ocr_reader = screen_ocr.Reader.create_reader(backend="easyocr")
    while True:
        results = ocr_reader.read_screen(bounding_box=(16, 303, 778, 375))
        parse(results.as_string())
        counter += 1
        if counter >= 10:
            ahk.send("/")
            ahk.send("{BS}")
            ahk.send("{BS}")
            counter = 0

def parse(result):
    # try:
    if "lig" in result.lower():
        send_stats(result.split("devoured")[1].strip(), "Luminosity", "1,200,000,000")
        return
    
    
    result = result[result.find("["):]
    result = result.replace("[Global]: ", "")
    if "tru" in result.lower() or "dis" in result.lower():
        send_stats(result.split("has")[0].strip(), "Oblivion", "2,000 (from oblivion potion)")
        return
    
    split = result.split("HAS FOUND")
    split[0] = split[0].strip()
    split[1] = split[1].strip()
    global last_user
    if split[0] == last_user:
        return
    else:
        last_user = split[0]
    # except:
    #     print("parse fail")
    #     return
    for aura in globals:
        if aura["check"] in split[1].lower():
            send_stats(split[0], aura["name"], aura["rarity"])
            break


embeds = []


def send_stats(username, aura_name, roll_chance):
    webhook_url = "https://discord.com/api/webhooks/1310067262249762926/Nehjc4FvdD8ceRSe1Nk90JP9v4ql4miJhIqF_YVCL4AOXDIcZQSI8R-GUE_5vvdFoCwD"
    embed_limit = 1
    global embeds
    embeds.append(
        {
            "description" : "1 in " + roll_chance + "\n\nTime Discovered\n<t:" + str(int(datetime.datetime.now().timestamp())) + ":f>",
            "author" : {
                "name": username
            },
            "title": username + " has found " + aura_name,
            # "color": webhook_color
        }
    )
    if len(embeds) >= embed_limit:
        # Send all embeds in a single request
        data = {
            "username" : "Genesis Stats Tracker",
            "embeds": embeds
        }


        try:
            result = requests.post(webhook_url, json = data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        except:
            print("send error")
        else:
            pass
        embeds.clear() 

def start():
    global main_process
    global running
    if running == True:
        return
    else:
        running = True
    
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
