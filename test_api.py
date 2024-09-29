import unittest
from __init__ import create_app
from config import TestConfig
from exts import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.create_all()
    
    def test_hello_world(self):
        hello_response = self.client.get("/user/hello")

        json = hello_response.json
        #print(json)

        self.assertEqual(json, {"message":"Hello world."})

    def test_signup(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"new",
                "user_email": "test@mail.com",
                "user_password": "123",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )
        login_response = self.client.post("/auth/login",
            json={
                "user_name":"new",
                "user_password": "123"
            }
        )
        
        json = signup_response.json
        #print(json)
        status_code = signup_response.status_code
        self.assertEqual(status_code, 201)

    def test_login(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"testnew",
                "user_email": "test@mail.com",
                "user_password": "123",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )
        login_response = self.client.post("/auth/login",
            json={
                "user_name":"testnew",
                "user_password": "123",
            }
        )
        
        json = login_response.json
        #print(json)

        status_code = login_response.status_code
        self.assertEqual(status_code, 200)

    def test_get_users(self):
        response = self.client.get("/user/users")
        
        #print(response.json)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_user(self):
        user_name = "new"
        response = self.client.get(f"/user/{user_name}")

        status_code = response.status_code
        #print(status_code)
        self.assertEqual(status_code, 404)

    def test_create_user(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"new",
                "user_email": "test@mail.com",
                "user_password": "123",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )
        
        login_response = self.client.post("/auth/login",
            json={
                "user_name":"new",
                "user_password": "123",
            }
        )

        access_token = login_response.json["access_token"]
        user_name = "new"
        create_user_response = self.client.get(f"user/{user_name}",
                                             headers={
                                                 "Authorization": f"Bearer {access_token}" 
                                             })
        status_code = create_user_response.status_code
        self.assertEqual(status_code, 200)
    
    def test_update_user(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"new",
                "user_email": "test@mail.com",
                "user_password": "123",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )
        login_response = self.client.post("/auth/login",
            json={
                "user_name":"new",
                "user_password": "123",
            }
        )
        
        access_token = login_response.json["access_token"]
        user_name = "new"
        create_user_response = self.client.get(f"user/{user_name}")
        status_code = create_user_response.status_code
        
        update_response = self.client.put(f"user/{user_name}",
                                          json={
                                                "user_name":"new",
                                                "user_email": "test@mail.com",
                                                "user_password": "123",
                                                "user_firstname": "first update",
                                                "user_lastname": "last update",
                                                "user_address": ""
                                                },
                                          headers={
                                              "Authorization": f"Bearer {access_token}" 
                                          },)
        status_code = update_response.status_code
        self.assertEqual(status_code, 200)

    def test_delete_user(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"new",
                "user_email": "test@mail.com",
                "user_password": "123",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )
        login_response = self.client.post("/auth/login",
            json={
                "user_name":"new",
                "user_password": "123",
            }
        )
        
        access_token = login_response.json["access_token"]
        user_name = "new"
        create_user_response = self.client.get(f"user/{user_name}")

        delete_response = self.client.delete(f"user/{user_name}",
                                             headers={
                                                 "Authorization": f"Bearer {access_token}" 
                                             })
        status_code = delete_response.status_code
        self.assertEqual(status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def testAddContact(self):
        signup_response = self.client.post("/auth/signup",
            json={
                "user_name":"newly",
                "user_email": "test@mail.com",
                "user_password": "12345678",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )

        signup_response_2 = self.client.post("/auth/signup",
            json={
                "user_name":"new_2",
                "user_email": "mest@mail.com",
                "user_password": "12345678",
                "user_firstname": "first",
                "user_lastname": "last",
                "user_address": ""
            }
        )

        login_response = self.client.post("/auth/login",
            json={
                "user_name":"newly",
                "user_password": "12345678",
            }
        )
        access_token = login_response.json["access_token"]
        user_name = "newly"
        create_user_response = self.client.get(f"user/{user_name}",
                                             headers={
                                                 "Authorization": f"Bearer {access_token}" 
                                             })
        status_code = create_user_response.status_code
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
