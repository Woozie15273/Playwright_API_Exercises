# Automated API Query Suite with Playwright

This project demonstrates a comprehensive end-to-end API testing framework built on the [Fake Store API](https://fakestoreapi.com/). It leverages Playwright for automation, Faker for dynamic data generation, and Python for test orchestration. The suite is designed to validate core API functionalities across authentication, carts, products, and users.

---

## Key Features

- **Dynamic Data Generation**: User payloads created on the fly using Faker.  
- **Centralized API Client**: Simplifies request handling and response validation.  
- **Modular Test Design**: Organized by resource type for scalability and clarity.  
- **Error Handling**: Ensures robust validation of negative scenarios.  

---

## Prerequisites

- **Python**: 3.14.0  
- **Playwright**: Latest version  
- **Faker**: [Documentation](https://faker.readthedocs.io/en/master/index.html)  

---

## Project Structure

| Directory / File       | Description                                |
|------------------------|--------------------------------------------|
| `/tests`               | Test cases grouped by resources offered by Fake Store API |
| `/utility/settings.py` | Stores global variables                    |
| `/utility/data_generator.py` | Generates user payloads dynamically   |
| `/utility/api_client.py`     | Centralized API operation class       |


---

## Test Coverage

### Authentication
1. Validate user login with valid credentials.  
2. Validate user cannot log in with unauthorized credentials.  
3. Validate login fails when a mandatory field is missing in the payload.  

### Carts
1. Validate `/carts/:id` returns the same cart as listed in `/carts`.  
2. Validate every product referenced in a cart exists in `/products`.  
3. Validate every cart references a valid user ID from `/users`.  
4. Validate every cart contains at least one product with a positive quantity.  
5. Validate a new cart cannot be created with a duplicate cart ID.  
6. Validate `POST` and `PUT` return a 400 error when mandatory fields are missing.  

### Products
1. Validate product categories meet expected values.  
2. Validate product price format in the database.  
3. Validate each product has a unique ID.  
4. Validate `/products/:id` returns the same product as listed in `/products`.  
5. Validate every category contains at least one product.  

### Users
1. Validate user IDs are unique.  
2. Validate `/users/:id` returns the same user as listed in `/users`.  
3. Validate email format in the database.  
4. Validate `POST` and `PUT` return a 400 error when mandatory fields are missing.  