import json
from datetime import datetime, date
from flask import Flask, request, jsonify

app = Flask(__name__)

class Patient(object):
	def __init__(self, birthDate, zipCode, admissionDate, dischargeDate, notes):
		self.age = self.convert_birthdate_to_age(birthDate)
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

	def convert_birthdate_to_age(self, birthDate):
		_birthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()
		today = date.today()

		# relies on the fact that int(True) == 1 ad int(False) == 0
		age = today.year - _birthDate.year - ((today.month, today.day) < 
         (_birthDate.month, _birthDate.day))
		return "90+" if age > 89 else str(age)


@app.route('/')
def hello():
	return 'hello, world!'

@app.route('/api/safeharbor', methods=["POST"])
def safeharbor():
    json_data = request.get_json()
    patient = Patient.from_json(json_data)
    return patient.to_json()
