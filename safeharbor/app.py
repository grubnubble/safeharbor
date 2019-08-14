from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
	return 'hello, world!'

@app.route('/api/safeharbor', methods=["POST"])
def safeharbor():
    json_data = request.get_json()
    email = json_data['email']
    password = json_data['password']
    return jsonify(email, password)