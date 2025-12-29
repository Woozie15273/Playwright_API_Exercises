from playwright.sync_api import APIRequestContext
from utility.settings import *

class APIClient:
        
    def __init__(self, request_context: APIRequestContext, logger):
        self._context = request_context
        self.logger = logger

    # --- Products ---

    def get_all_products(self):
        self.logger.info("GET All Products")
        return self._context.get(PRODUCT_ENDPOINT)
    
    def get_products_by_id(self, prod_id: int):
        self.logger.info(f"GET product id: {prod_id}")
        return self._context.get(f"{PRODUCT_ENDPOINT}/{prod_id}")
    
    def create_products(self, payload: dict):
        self.logger.info(f"POST product with keys: {list(payload.keys())}")
        return self._context.post(PRODUCT_ENDPOINT, data = payload)
    
    def update_products(self, prod_id: int, payload: dict):
        self.logger.info(f"PUT product {prod_id} with keys: {list(payload.keys())}")
        return self._context.put(f"{PRODUCT_ENDPOINT}/{prod_id}", data = payload)
    
    def delete_products(self, prod_id: int):
        self.logger.info(f"DELETE product id: {prod_id}")
        return self._context.delete(f"{PRODUCT_ENDPOINT}/{prod_id}")

    # --- Carts ---

    def get_all_cart(self):
        self.logger.info("GET All Carts")
        return self._context.get(CART_ENDPOINT)
    
    def get_cart_by_id(self, cart_id: int):
        self.logger.info(f"GET cart id: {cart_id}")
        return self._context.get(f"{CART_ENDPOINT}/{cart_id}")
    
    def create_cart(self, payload: dict):
        self.logger.info(f"POST cart with keys: {list(payload.keys())}")
        return self._context.post(CART_ENDPOINT, data = payload)
    
    def update_cart(self, cart_id: int, payload: dict):
        self.logger.info(f"PUT cart {cart_id} with keys: {list(payload.keys())}")
        return self._context.put(f"{CART_ENDPOINT}/{cart_id}", data = payload)
    
    def delete_cart(self, cart_id: int):
        self.logger.info(f"DELETE cart id: {cart_id}")
        return self._context.delete(f"{CART_ENDPOINT}/{cart_id}")

    # --- Users ---

    def get_all_users(self):
        self.logger.info("GET All Users")
        return self._context.get(USER_ENDPOINT)
    
    def get_user_by_id(self, uid: int):
        self.logger.info(f"GET user id: {uid}")
        return self._context.get(f"{USER_ENDPOINT}/{uid}")
    
    def create_user(self, payload: dict):
        self.logger.info(f"POST user with keys: {list(payload.keys())}")
        return self._context.post(USER_ENDPOINT, data = payload)
    
    def update_user(self, uid: int, payload: dict):
        self.logger.info(f"PUT user {uid} with keys: {list(payload.keys())}")
        return self._context.put(f"{USER_ENDPOINT}/{uid}", data = payload)
    
    def delete_user(self, uid: int):
        self.logger.info(f"DELETE user id: {uid}")
        return self._context.delete(f"{USER_ENDPOINT}/{uid}")

    # --- Auth ---

    def auth_a_user(self, payload: dict):
        self.logger.info(f"POST user with fields: {list(payload.values())}")
        return self._context.post(AUTH_ENDPOINT, data = payload)


