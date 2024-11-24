import requests

# Replace with your webhook URL
webhook_url = "https://discord.com/api/webhooks/1310067262249762926/Nehjc4FvdD8ceRSe1Nk90JP9v4ql4miJhIqF_YVCL4AOXDIcZQSI8R-GUE_5vvdFoCwD"

# List of embeds to send in one request
embeds = [
    {
        "title": "Message 1",
        "description": "Hello, Discord!"
    },
    {
        "title": "Message 2",
        "description": "This is message number 2"
    },
    {
        "title": "Message 3",
        "description": "And here's message number 3"
    }
]

# Send all embeds in a single request
data = {
    "embeds": embeds
}

response = requests.post(webhook_url, json=data)
if response.status_code == 204:
    print("All messages sent successfully!")
else:
    print(f"Failed to send messages, Response: {response.status_code}")
