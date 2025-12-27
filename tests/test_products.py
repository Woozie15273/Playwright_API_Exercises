from collections import Counter
from tests.conftest import validate_id_consistency, validate_unique_identifier
from utility.settings import PRODUCT_CATEGORIES

class TestProducts:

    def test_get_all_categories(self):
        """ For data generator: get all unique product categories from the response """ 
        
        unique_categories = {entry["category"] for entry in self._get_re_json_of_all_products()}
        assert unique_categories == PRODUCT_CATEGORIES, f"Got {unique_categories}, expected {PRODUCT_CATEGORIES}"

    def test_product_price_validity(self):
        """ Check type and value -> positive float or integer """

        invalid_prod = []
        for product in self._get_re_json_of_all_products():
            prod_id = product.get("id")
            price = product.get("price")

            if not isinstance(price, (float, int)) or float(price) <= 0:
                invalid_prod.append(prod_id, price)
            
        assert not invalid_prod, (f"Invalid product prices found: {invalid_prod}")

    def test_unique_product_id(self):
        """ Get all products that their ID are not unique """        

        json = self._get_re_json_of_all_products()
        duplicated_prod = validate_unique_identifier(json, "id", "title")
        assert not duplicated_prod, f"Duplicate product IDs found: {duplicated_prod}"

    def test_single_product_consistency(self):
        """ Ensure /products/:id returns the same as found in /products. """
        
        json_all_products = self._get_re_json_of_all_products()
        failures = validate_id_consistency(json_all_products, self._get_re_json_for_product)
        assert not failures, "Product mismatches found:\n" + "\n".join(failures)

    def test_category_coverage(self):
        """ Ensure every category has at least one product """
        
        counts = Counter(prod.get("category") for prod in self._get_re_json_of_all_products())
        failures = [cat for cat, count in counts.items() if count == 0]
        assert not failures, f"Empty categories found: {failures}"

    # --- Helpers ---

    def _get_re_json_of_all_products(self) -> list:
        re = self.client.get_all_products()
        assert re.status == 200
        return re.json()
    
    def _get_re_json_for_product(self, id: int) -> list:
        re = self.client.get_products_by_id(id)
        assert re.status == 200
        return re.json()
    
