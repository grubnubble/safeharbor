from safeharbor.app import app

def test_hello():
	with app.test_client() as client:
	    response = client.get("/")
	    assert response.status_code == 200

def test_safeharbor():
	with app.test_client() as client:
		response = client.post("api/safeharbor",
			json={
				"email": "montana@gmail.com",
				"password": "123456"
			})
		assert response.status_code == 200