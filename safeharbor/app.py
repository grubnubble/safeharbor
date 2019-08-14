import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class Patient(object):
	def __init__(self, birthDate, zipCode, admissionDate, dischargeDate, notes):
		self.birthDate = birthDate
		self.zipCode = zipCode
		self.admissionDate = admissionDate
		self.dischargeDate = dischargeDate
		self.notes = notes

	@staticmethod
	def from_json(data):
		return Patient(
			data["birthDate"],
			data["zipCode"],
			data["admissionDate"],
			data["dischargeDate"],
			data["notes"])

	def to_json(self):
		return json.dumps(self.__dict__)

@app.route('/')
def hello():
	return 'hello, world!'

@app.route('/api/safeharbor', methods=["POST"])
def safeharbor():
    json_data = request.get_json()
    patient = Patient.from_json(json_data)
    return patient.to_json()
