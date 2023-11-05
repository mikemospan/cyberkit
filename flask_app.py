from flask import Flask, request, render_template, jsonify
import requests, socket

app = Flask(__name__)

def read_counter_from_file(filename):
    try:
        with open(filename, "r") as file:
            counter = int(file.read())
            return counter
    except FileNotFoundError:
        return 0

def write_counter_to_file(filename, counter):
    with open(filename, "w") as file:
        file.write(str(counter))

counter = read_counter_from_file("counter.txt")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/metadata')
def metadata():
    clientIp = request.headers['X-Forwarded-For']
    hostName = socket.gethostname()
    referrer = request.referrer
    hostIp = requests.get('https://api.ipify.org').content.decode('utf8')

    return render_template('metadata.html', referrer=referrer, hostName=hostName,
                           clientIp=clientIp, hostIp=hostIp)

@app.route("/xss")
def xss():
    return render_template("xss.html")

@app.route("/keylogger")
def keylogger():
    return render_template("keylogger.html")

@app.route("/consent")
def consent():
    return render_template("consent.html")

@app.route('/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    write_counter_to_file("counter.txt", counter)
    return jsonify({'counter': counter})

@app.route('/get_counter', methods=['GET'])
def get_counter():
    return jsonify({'counter': counter})