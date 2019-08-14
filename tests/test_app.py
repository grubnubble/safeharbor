from safeharbor.app import app

client = app.test_client()

def test_hello():
    response = client.get("/")
    assert response.status_code == 200

def test_safeharbor():
	response = client.post("api/safeharbor",
		json={
			"email": "montana@gmail.com",
			"password": "123456"
		})
	assert response.status_code == 200