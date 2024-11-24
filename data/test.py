import requests
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