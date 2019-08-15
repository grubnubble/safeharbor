import json
from safeharbor.app import app, Patient

client = app.test_client()
patient_data = {
	"birthDate": "2000-01-01",
    "zipCode": "10013",
    "admissionDate": "2019-03-12",
    "dischargeDate": "2019-03-14",
    "notes": "Patient with ssn 123-45-6789 previously presented under different ssn"
}
patient = Patient.from_json(patient_data)
CSV_FILE = 'test_data.csv'

def test_hello():
    response = client.get("/")
    assert response.status_code == 200

def test_safeharbor():
	response = client.post("api/safeharbor",
		json=patient_data)
	assert response.status_code == 200
	assert json.loads(response.data)["age"] == "19"
	assert json.loads(response.data)["zipCode"] == "100XX"
	assert json.loads(response.data)["admissionDate"] == "2019"
	assert json.loads(response.data)["dischargeDate"] == "2019"
	assert json.loads(response.data)["notes"] == "Patient with ssn XXX-XX-XXXX previously presented under different ssn"

def test_convert_birthdate_to_age_90_plus():
	old_patient_data = {
		"birthDate": "1900-01-01",
	    "zipCode": "10013",
	    "admissionDate": "2019-03-12",
	    "dischargeDate": "2019-03-14",
	    "notes": "A patient over 89 years old"
	}
	patient = Patient.from_json(old_patient_data)

	patient.convert_birthdate_to_age(patient_data["birthDate"])
	assert patient.age == "90+"
	assert not hasattr(patient, "birthDate")

def test__create_zipcode_to_population_dict():
	expected = {"010": 30951, "012": 485, "014": 11497}
	result = Patient._create_zipcode_to_population_dict(patient, CSV_FILE)
	assert type(result) == dict
	assert result == expected

# TODO
def test_return_00000_when_population_less_than_20k():
	pass

def test_de_identify_email():
	expected = "the patient's email is XXX@XXX.XXX yes it is"
	result = Patient.de_identify_notes(patient, "the patient's email is patient@hospital.org yes it is")
	assert result == expected

def test_de_identify_social_sec():
	expected = "the patient's ssn is XXX-XX-XXXX yes it is"
	result = Patient.de_identify_notes(patient, "the patient's ssn is 789-56-1234 yes it is")
	assert result == expected

def test_de_identify_phone():
	# TODO cover other forms phone numbers can take
	expected = "the patient's phone is (XXX) XXX-XXXX yes it is"
	result = Patient.de_identify_notes(patient, "the patient's phone is (309) 956-1234 yes it is")
	assert result == expected

def test_de_identify_dates():
	# TODO cover other forms dates can take
	expected = "the patient's birth date is 1996 yes it is"
	result = Patient.de_identify_notes(patient, "the patient's birth date is 1996-05-21 yes it is")
	assert result == expected