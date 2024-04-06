import requests

SERVER_URL = "http://localhost:8000"

def send_message(content: str):
    response = requests.post(f"{SERVER_URL}/send_message/", json={"content": content})
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")

def get_messages():
    response = requests.get(f"{SERVER_URL}/get_messages/")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get messages")
        return []

if __name__ == "__main__":
    send_message("Hello, server!")
    messages = get_messages()
    for message in messages:
        print(message["content"])