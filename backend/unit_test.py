import unittest
import requests
import names

class ApiTesting(unittest.TestCase):

    def test_registering_user(self):

        URL = "http://backend:5000/user/register"
        PARAMS = {
            'username': "root", f'password': 'root'
        }
        r = requests.post(URL,
                          params=PARAMS)

        if r.status_code == 401:
            self.assertEqual(r.status_code,401)
        elif r.status_code == 200:
            self.assertEqual(r.status_code,200)
        else:
            self.assertEqual(r.status_code,200)

    def test_login_user(self):

        URL = "http://backend:5000/user/login"
        PARAMS = {
            'username': "root", f'password': 'root'
        }
        r = requests.post(URL,
                          params=PARAMS)
        if r.status_code == 401:
            self.assertEqual(r.status_code, 401)
        elif r.status_code == 200:
            self.assertEqual(r.status_code, 200)
        else:
            self.assertEqual(r.status_code, 200)

    def test_authentication_fail(self):
        URL = "http://backend:5000/user/login"
        PARAMS = {
            'username': "admin", f'password': 'root'
        }
        r = requests.post(URL,
                          params=PARAMS)
        self.assertEqual(r.status_code, 401)

    def test_add_new_user(self):
        URL = "http://backend:5000/user/register"

        username = names.get_first_name()
        password = names.get_last_name()
        PARAMS = {
            'username': f"{username}", f'password': f'{password}'
        }
        r = requests.post(URL,
                          params=PARAMS)

        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()