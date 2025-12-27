from faker import Faker
import random

class DataGenerator:

    def __init__(self):
        self.faker = Faker()
    
    # --- Users ---
    
    def get_id(self) -> int:
        return random.randint(1000, 1999)
    
    def generate_user(self) -> dict:
        username = self.get_username()

        return {
            "id" : self.get_id(),
            "username" : username,
            "email": self.get_email(username),
            "password": self.get_password()
        }
    
    def get_username(self) -> str:
        return "".join(map(str, self.faker.passport_owner()))
    
    def get_email(self, username: str):
        email = username + self.faker.free_email_domain()
        return email
    
    def get_password(self):
        return self.faker.password(length = 8)
