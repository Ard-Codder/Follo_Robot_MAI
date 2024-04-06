from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.json["message"]
    messages.append(message)
    print(message)
    return jsonify({"status": "success"}), 200

@app.route("/get_message", methods=["GET"])
def get_message():
    if messages:
        return jsonify({"message": messages.pop(0)})
    else:
        return jsonify({"message": "Нет новых сообщений."})

if __name__ == "__main__":
    app.run(debug=True)