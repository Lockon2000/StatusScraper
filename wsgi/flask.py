from datetime import datetime

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def main():
    return 'Webhook Root'

@app.route('/nfon', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        logfile = open("logs/nfon-webhook.log", "a")
        logfile.write("\n\nGot payload on " + str(datetime.now()) + "\n")
        logfile.write(str(request.get_json()))
        return 'Request Successful'

    elif request.method == 'GET':
        return 'NFON Endpoint'


if __name__ == "__main__":
    app.run()