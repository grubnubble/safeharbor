import json
from safeharbor.app import app

client = app.test_client()
patient_data = {
	"birthDate": "2000-01-01",
    "zipCode": "10013",
    "admissionDate": "2019-03-12",
    "dischargeDate": "2019-03-14",
    "notes": "Patient with ssn 123-45-6789 previously presented under different ssn"
}

def test_hello():
    response = client.get("/")
    assert response.status_code == 200

def test_safeharbor():
	response = client.post("api/safeharbor",
		json=patient_data)
	assert response.status_code == 200
	assert json.loads(response.data)["birthDate"] == patient_data["birthDate"]
	assert json.loads(response.data)["zipCode"] == patient_data["zipCode"]
	assert json.loads(response.data)["admissionDate"] == patient_data["admissionDate"]
	assert json.loads(response.data)["dischargeDate"] == patient_data["dischargeDate"]
	assert json.loads(response.data)["notes"] == patient_data["notes"]
