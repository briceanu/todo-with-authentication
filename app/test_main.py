from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# def test_sign_up():
#     response = client.post('/user/sign_up',
#                            json={'username':'marian','password':'marian123','confirm_password':'marian123'}) 


#     assert response.status_code == 200
#     assert response.json() == {"success": "your account has been created"}



def test_get_access_token():
    response = client.post('/user/sign_in',data={'username':'gigi','password':'gigi123'})

    assert response.status_code == 200
    assert response.json()['access_token']

 

 
 

def test_list_all_todos():
    response = client.get('/todo/all')
    assert response.status_code == 200
    assert response.json()[0]['title'] == "my first day at learning fastapi"
    assert response.json()[0]['content'] == "this the math in the fastAPI environment"






# def test_remove_a_todo():
#     todo_id = 'b754f61f-0b0c-4f17-9211-5788fae51fe2'

#     authorization = { 
#         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnaWdpIiwiZXhwIjoxNzQyODIyMTM0fQ.go-Mmp1Aeu8JfjrAfNgKYK0OY0qQ_D3TSeszESQ0fWc", 
#         "token_type": "bearer"
#     }

#     headers = {
#         "Authorization": f"Bearer {authorization['access_token']}",
#         "Content-Type": "application/json"
#     }

#     body = {
#         "todo_id": todo_id
#     }

#     # Use 'json' instead of 'data' for a DELETE request
#     response = client.delete('/todo/remove', json=body, headers=headers)

#     assert response.status_code == 200
#     assert response.json() == {"success": "todo removed"}



