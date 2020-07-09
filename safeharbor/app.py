import json, csv, re
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
		self.notes = self.de_identify_notes(notes)

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
		birthDate = datetime.strptime(birthDate, '%Y-%m-%d').date()
		today = date.today()

		# relies on the fact that int(True) == 1 and int(False) == 0
		age = today.year - birthDate.year - ((today.month, today.day) < 
         (birthDate.month, birthDate.day))
		return "90+" if age > 89 else str(age)

	def get_year(self, date):
		return str(datetime.strptime(date, '%Y-%m-%d').date().year)

	def de_identify_zipcode(self, zipCode):
		populationDict = self._create_zipcode_to_population_dict(self.CSV_FILE)
		key = zipCode[:3]
		if populationDict[key] < 20000:
			return '00000'
		else:
			return key + "XX"

	def de_identify_notes(self, notes):
		# TODO make sure you find all matches
		email_replaced = re.sub(r'[\w\.-]+@[\w\.-]+', "XXX@XXX.XXX", notes)
		ssn_replaced = re.sub(r'[0-9]{3}-[0-9]{2}-[0-9]{4}', "XXX-XX-XXXX", email_replaced)
		phone_replaced = re.sub(r'\([0-9]{3}\) [0-9]{3}-[0-9]{4}', "(XXX) XXX-XXXX", ssn_replaced)

		dateMatch = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', phone_replaced)
		dates_replaced = re.sub(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', self.get_year(dateMatch.group(0)), phone_replaced) if dateMatch else phone_replaced

		return dates_replaced

	def _create_zipcode_to_population_dict(self, csvfile):
		""" Takes a csv file and returns a dictionary where
			the keys are the first three digits of the zipCode
			and the values are the total population from all zipcodes
			starting with those three digits """
		data = {}
		# TODO refactor: check that the population is less than 20K before adding
		with open(csvfile) as csvfile:
			popreader = csv.reader(csvfile, delimiter=",")
			for row in popreader:
				key = row[0][:3]
				if key in data:
					data[key] = int(data[key]) + int(row[1])
				else:
					try:
						data[key] = int(row[1])
					except ValueError:
						# ignore first row in the file
						pass
			return data


@app.route('/')
def hello():
	return 'hello, world!'

@app.route('/api/safeharbor', methods=["POST"])
def safeharbor():
    json_data = request.get_json()
    patient = Patient.from_json(json_data)
    return patient.to_json()
