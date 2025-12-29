import pytest
from tests.conftest import validate_id_consistency
from random import choice

class TestCarts:

    def test_single_cart_consistency(self):
        """ Ensure /carts/:id returns the same cart as found in /carts. """

        json_all_users = self._get_re_json_of_all_carts()
        failures = validate_id_consistency(json_all_users, self._get_re_json_for_cart)
        self.logger.info(f"Carts mismatches found:{"\n".join(failures)}")
        assert not failures        
    
    def test_cart_product_reference_integrity(self):
        """Verify that every product referenced in a cart actually exists in /products. """

        invalid_products = self._helper_cart_reference_integrity_bulk("productId")
        self.logger.info(f"Invalid product references found: {invalid_products}")
        assert not invalid_products        

    def test_cart_user_reference_integrity(self):
        """Verify that every cart references a valid user ID that exists in /users. """

        invalid_users = self._helper_cart_reference_integrity_bulk("userId")
        self.logger.info(f"Invalid user references found: {invalid_users}")
        assert not invalid_users        

    def test_cart_product_quantity_validation(self):
        ''' Ensure that every cart has at least one product with positive quantity. '''
        
        invalid_cart_ids = []

        for cart in self._get_re_json_of_all_carts():
            cart_id = cart.get("id")
            products = cart.get("products", [])
            
            # Check: non-empty AND at least one product with quantity > 0
            if not products or not any(p.get("quantity", 0) > 0 for p in products):
                invalid_cart_ids.append(cart_id)

        # Final assertion
        self.logger.info(f"Found carts with invalid products list: {invalid_cart_ids}")
        assert not invalid_cart_ids        

    def test_create_cart_unique_id_validation(self):
        existing_cart = self._get_a_random_cart()
        re = self.client.create_cart(existing_cart)
        actual =  re.status
        expect = 400
        self.logger.info(f"Actual: {actual}; Expect: {expect}")
        assert actual == 400, f"A new cart shouldn't be created on a duplicated cart ID"


    @pytest.mark.parametrize(
        "missing_field, expected_status",
        [
            pytest.param(None, 200, id="all_fields_present"),
            pytest.param("id", 400, id="missing_id"),
            pytest.param("userId", 400, id="missing_userId"),
            pytest.param("date", 400, id="missing_date"),
            pytest.param("products", 400, id="missing_products"),
        ]
    )
    def test_update_cart(self, missing_field, expected_status):
        payload = self._get_a_random_cart()
        cart_id = payload.get("id")

        if missing_field:
            payload.pop(missing_field, None)

        re = self.client.update_cart(cart_id, payload)
        actual_status = re.status

        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status}; When missing {missing_field}")
        assert re.status == expected_status        



    @pytest.mark.parametrize(
        "missing_field, expected_status",
        [
            pytest.param(None, 201, id="all_fields_present"),
            pytest.param("id", 400, id="missing_id"),
            pytest.param("userId", 400, id="missing_userId"),
            pytest.param("date", 400, id="missing_date"),
            pytest.param("products", 400, id="missing_products"),
        ]
    )
    def test_create_cart_missing_field_validation(self, _mirror_a_new_cart, missing_field, expected_status):
        new_cart = _mirror_a_new_cart

        if missing_field:
            new_cart.pop(missing_field, None)

        re = self.client.create_cart(new_cart)
        actual_status = re.status

        self.logger.info(f"Actual: {actual_status}; Expect: {expected_status}; When missing {missing_field}")
        assert actual_status == expected_status

    # --- Helpers ---
    
    def _get_a_new_cart_id(self) -> int:
        unique_id = {entry["id"] for entry in self._get_re_json_of_all_carts()}
        return max(unique_id) + 1
    
    @pytest.fixture(scope="function")
    def _mirror_a_new_cart(self) -> dict:
        existing_cart = self._get_a_random_cart()
        return {**existing_cart, "id": self._get_a_new_cart_id()}


    def _get_a_random_cart(self) -> dict:
        """ e.g. {'id': 5, 'userId': 3, 'date': '2020-03-01T00:00:00.000Z', 'products': [{'productId': 7, 'quantity': 1}, {'productId': 8, 'quantity': 1}], '__v': 0} """
        re = self._get_re_json_of_all_carts()
        return choice(re)

    def _helper_cart_reference_integrity_bulk(self, field_name: str):
        """
        Validate that all IDs referenced in carts exist via bulk API calls.
        field_name: 'userId' or 'productId'
        """
        carts_json = self._get_re_json_of_all_carts()

        # Fetch all users or products once
        support_json = (
            self.client.get_all_users().json()
            if field_name == "userId"
            else self.client.get_all_products().json()
        )

        # Build set of valid IDs from support_json
        valid_ids = {entry.get("id") for entry in support_json if "id" in entry}

        # Collect unique IDs from carts
        if field_name == "userId":
            unique_ids = {c.get("userId") for c in carts_json if "userId" in c}
            invalid_entries = {
                uid: [c["id"] for c in carts_json if c.get("userId") == uid]
                for uid in unique_ids if uid not in valid_ids
            }
        elif field_name == "productId":
            unique_ids = {
                p.get("productId")
                for c in carts_json
                for p in c.get("products", [])
                if "productId" in p
            }
            invalid_entries = {
                uid: [c["id"] for c in carts_json if any(p.get("productId") == uid for p in c.get("products", []))]
                for uid in unique_ids if uid not in valid_ids
            }
        else:
            raise ValueError(f"Unsupported field_name: {field_name}")

        return invalid_entries

    def _get_re_json_of_all_carts(self) -> list:
        re = self.client.get_all_cart()
        assert re.status == 200
        return re.json()
    
    def _get_re_json_for_cart(self, id: int) -> list:
        re = self.client.get_cart_by_id(id)
        assert re.status == 200
        return re.json() 
    