import requests

SERVER_URL = "http://localhost:5000"

def send_message(message):
    response = requests.post(f"{SERVER_URL}/send_message", json={"message": message})
    if response.status_code == 200:
        print("Сообщение успешно отправлено.")
    else:
        print("Ошибка при отправке сообщения:", response.text)

def get_message():
    response = requests.get(f"{SERVER_URL}/get_message")
    if response.status_code == 200:
        return response.json()["message"]
    else:
        print("Ошибка при получении сообщения:", response.text)
        return None

send_message('Hellow')
get_message()