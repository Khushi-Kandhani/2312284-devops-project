import pytest

def test_create_and_get_student(client):
    # 1. Prepare payload with your personalized information
    payload = {
        "id": 1,
        "name": "Khushi Kandhani", 
        "reg_no": "2312284", 
        "email": "bscs2312284@szabist.pk"
    }
    
    # 2. Submit POST request to create the student record
    response = client.post("/students/", json=payload)
    # Checks for both 201 Created or 200 OK depending on your router implementation
    assert response.status_code in [200, 201]

    # 3. Submit GET request to verify the student array has the new entry
    get_response = client.get("/students/")
    assert get_response.status_code == 200
    
    # Assert that at least one student is present in the database array
    students_list = get_response.json()
    assert len(students_list) >= 1
    
    # Verify that your details match perfectly in the response data
    latest_student = students_list[-1]  # Grab the most recently added student
    assert latest_student["name"] == "Khushi Kandhani"
    assert latest_student["reg_no"] == "2312284"
    assert latest_student["email"] == "bscs2312284@szabist.pk"
