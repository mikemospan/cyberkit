from flask import Flask, request, render_template, jsonify
import requests, socket

app = Flask(__name__)

counter = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/keylogger")
def keylogger():
    return render_template("keylogger.html")

@app.route('/metadata')
def metadata():
    hostIp = request.remote_addr
    hostName = socket.gethostname()
    clientIp = socket.gethostbyname(hostName)
    referrer = request.referrer
    publicIp = requests.get('https://api.ipify.org').content.decode('utf8')

    return render_template('metadata.html', referrer=referrer, hostName=hostName, hostIp=hostIp,
                           clientIp=clientIp, publicIp=publicIp)

@app.route('/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    print(counter)
    return jsonify({'counter': counter})

@app.route('/get_counter', methods=['GET'])
def get_counter():
    return jsonify({'counter': counter})

if __name__ == "__main__":
    app.run(debug=True)