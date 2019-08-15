import json, csv
from datetime import datetime, date
from flask import Flask, request, jsonify

app = Flask(__name__)

class Patient(object):
	CSV_FILE = 'population_by_zcta_2010.csv'

	def __init__(self, birthDate, zipCode, admissionDate, dischargeDate, notes):
		self.age = self.convert_birthdate_to_age(birthDate)
		self.zipCode = self.de_identify_zipcode(zipCode)
		self.admissionDate = self.get_year(admissionDate)
		self.dischargeDate = self.get_year(dischargeDate)
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

	def get_year(self, date):
		return str(datetime.strptime(date, '%Y-%m-%d').date().year)

	def strip_last_two_digits(self, zipCode):
		return zipCode[:3] + "XX"

	def de_identify_zipcode(self, zipCode):
		csvDict = csv_to_dictionary(self.CSV_FILE)
		return self.strip_last_two_digits(zipCode)

def csv_to_dictionary(csvfile):
	data = {}
	with open(csvfile) as csvfile:
		popreader = csv.reader(csvfile, delimiter=",")
		for row in popreader:
			data[row[0]] = row[1]
		return data


@app.route('/')
def hello():
	return 'hello, world!'

@app.route('/api/safeharbor', methods=["POST"])
def safeharbor():
    json_data = request.get_json()
    patient = Patient.from_json(json_data)
    return patient.to_json()
