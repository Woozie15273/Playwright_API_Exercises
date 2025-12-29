from random import choice
import pytest

class TestAuth:

    # --- Helpers --- 
    
    def _get_credentials(self) -> dict:
        ''' Get all users from API '''
        re_get_users = self.client.get_all_users()        
        assert re_get_users.status == 200

        credentials = {
            entry["username"]: entry["password"]
            for entry in re_get_users.json()
            if "username" in entry and "password" in entry
        }

        return credentials
    
    def _get_random_credential(self) -> dict:
        """ Randomly pick a username, password pair as a new dict """
        entries = self._get_credentials()
        user, password = choice(list(entries.items()))
        return {"username": user, "password": password}    

    def _valid_user(self, data_generator=None):
        return self._get_random_credential()

    def _unauthorized_user(self, data_generator):
        return {"username": data_generator.get_username(), "password": data_generator.get_password()}

    def _missing_password(self, data_generator=None):
        user = self._get_random_credential()
        return {"username": user["username"], "password": ""}

    def _missing_username(self, data_generator=None):
        user = self._get_random_credential()
        return {"username": "", "password": user["password"]}

    def _wrong_password(self, data_generator):
        user = self._get_random_credential()
        return {"username": user["username"], "password": data_generator.get_password()}

    def _wrong_username(self, data_generator):
        user = self._get_random_credential()
        return {"username": data_generator.get_username(), "password": user["password"]}

    # --- Test function ---

    @pytest.mark.parametrize(
        "builder, expected_status, message",
        [
            (_valid_user, 201, "Failed to login with correct credential"),
            (_unauthorized_user, 401, "Unauthorized user logged in successfully"),
            (_missing_password, 400, "Authorized user without password logged in successfully"),
            (_missing_username, 400, "Authorized user without username logged in successfully"),
            (_wrong_password, 401, "Authorized user with wrong password logged in successfully"),
            (_wrong_username, 401, "Authorized user with wrong username logged in successfully"),
        ],
        ids=[
            "valid-user",
            "unauthorized-user",
            "missing-password",
            "missing-username",
            "wrong-password",
            "wrong-username",
        ]
    )

    def test_auth_cases(self, builder, expected_status, message, data_generator):
        payload = builder(self, data_generator)
        re = self.client.auth_a_user(payload)
        actual_status = re.status

        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status}")
        assert actual_status == expected_status, message
        




