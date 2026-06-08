def test_create_and_get_student(client):
    payload = {"name": "John Doe", "reg_no": "123456", "email": "john@example.com"}
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    
    get_response = client.get("/students")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
