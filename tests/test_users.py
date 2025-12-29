import re
from tests.conftest import validate_id_consistency, validate_unique_identifier
import pytest
from random import choice

class TestUsers:
    
    def test_unique_user_id(self):
        """ Get all usernames that their ID are not unique """

        json = self._get_re_json_of_all_users()
        duplicated_uid = validate_unique_identifier(json, "id", "username")
        self.logger.info(f"Duplicate user IDs found: {duplicated_uid}")
        assert not duplicated_uid
    
    def test_single_user_consistency(self):
        """ Ensure /users/:id returns the same user as found in /users. """

        json_all_users = self._get_re_json_of_all_users()
        failures = validate_id_consistency(json_all_users, self._get_re_json_for_user)
        self.logger.info(f"User mismatches found: {"\n".join(failures)}")
        assert not failures

    def test_validate_email_format(self):
        '''
        Regex ensures a basic email format: one or more non-@ chars, then '@', 
        followed by one or more non-@ chars, a dot '.', and one or more non-@ chars.
        '''
        
        json_data = self._get_re_json_of_all_users()
        
        email_pattern = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
        invalid_pairs = []

        for user in json_data:
            user_id = user.get("id")
            email = user.get("email", "")

            if not email_pattern.match(email):
                invalid_pairs.append((user_id, email))

        self.logger.info(f"Invalid email formats found: {invalid_pairs}")
        assert not invalid_pairs

    # --- Parameterized TCs---

    @pytest.mark.parametrize(
        "missing_field, expected_status",
        [
            pytest.param(None, 201, id="all_fields_present"),
            pytest.param("id", 400, id="missing_id"),
            pytest.param("username", 400, id="missing_username"),
            pytest.param("email", 400, id="missing_email"),
            pytest.param("password", 400, id="missing_password"),
        ]
    )
    def test_post_user(self, data_generator, missing_field, expected_status):
        # Generate a valid payload
        payload = data_generator.generate_user()

        # Drop the field if testing a missing case
        if missing_field:
            payload.pop(missing_field, None)

        re = self.client.create_user(payload)
        actual_status = re.status        

        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status}; When missing {missing_field}")
        assert actual_status == expected_status


        

    @pytest.fixture(scope="function")
    def _valid_uid_and_payload(self, data_generator):
        # Generate a valid payload once
        payload = data_generator.generate_user()

        # Get a random user once
        re_get_users = self.client.get_all_users()
        assert re_get_users.status == 200
        users = re_get_users.json()
        uid = choice(users)["id"]

        return uid, payload.copy()  # return a fresh copy for each test
    
    @pytest.mark.parametrize(
        "missing_field, expected_status",
        [
            pytest.param(None, 200, id="all_fields_present"),
            pytest.param("id", 400, id="missing_id"),
            pytest.param("username", 400, id="missing_username"),
            pytest.param("email", 400, id="missing_email"),
            pytest.param("password", 400, id="missing_password"),
        ]
    )
    def test_update_user(self, _valid_uid_and_payload, missing_field, expected_status):
        uid, payload = _valid_uid_and_payload

        # Drop the field if testing a missing case
        if missing_field:
            payload.pop(missing_field, None)

        re = self.client.update_user(uid, payload)
        actual_status = re.status

        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status}; When missing {missing_field}")
        assert actual_status == expected_status



    @pytest.mark.parametrize(
        "uid, expected_status",
        [
            pytest.param("non-existent-id-12345", 400, id="invalid_uid"),
            pytest.param("", 404, id="empty_uid"),
        ]
    )
    def test_update_user_invalid_uid(self, data_generator, uid, expected_status):
        payload = data_generator.generate_user()
        re = self.client.update_user(uid, payload)
        actual_status = re.status
        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status} for uid='{uid}'")
        assert actual_status == expected_status


    # --- Helper ---

    def _get_re_json_of_all_users(self) -> list:
        re = self.client.get_all_users()
        assert re.status == 200
        return re.json()
    
    def _get_re_json_for_user(self, id: int) -> list:
        re = self.client.get_user_by_id(id)
        assert re.status == 200
        return re.json()    






