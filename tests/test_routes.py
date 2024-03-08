from unittest import TestCase
from service.models import Account
from service.common import status
from service.routes import app

BASE_URL = "/accounts"


class TestAccountService(TestCase):
    """Account Service Tests"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_create_account(self):
        """It should Create a new Account"""
        account_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "phone_number": "555-1234",
        }
        response = self.client.post(
            BASE_URL,
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_account = response.json
        self.assertEqual(new_account["name"], account_data["name"])
        self.assertEqual(new_account["email"], account_data["email"])
        self.assertEqual(new_account["address"], account_data["address"])
        self.assertEqual(new_account["phone_number"], account_data["phone_number"])

    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account_list = response.json
        self.assertIsInstance(account_list, list)

    def test_read_account(self):
        """It should Read a single Account"""
        account_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "phone_number": "555-1234",
        }
        create_response = self.client.post(
            BASE_URL,
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        account_id = create_response.json["id"]  # Fix here
        response = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_account = response.json
        self.assertEqual(retrieved_account["id"], account_id)

    def test_update_account(self):
        """It should Update an existing Account"""
        account_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "phone_number": "555-1234",
        }
        create_response = self.client.post(
            BASE_URL,
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        account_id = create_response.json["id"]  # Fix here
        updated_account_data = {
            "name": "Updated Name",
            "email": "updated.email@example.com",
            "address": "456 Updated St",
            "phone_number": "555-5678",
        }
        response = self.client.put(
            f"{BASE_URL}/{account_id}",
            json=updated_account_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_account = response.json
        self.assertEqual(updated_account["name"], updated_account_data["name"])
        self.assertEqual(updated_account["email"], updated_account_data["email"])
        self.assertEqual(updated_account["address"], updated_account_data["address"])
        self.assertEqual(updated_account["phone_number"], updated_account_data["phone_number"])

    def test_delete_account(self):
        """It should Delete an Account"""
        account_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "123 Main St",
            "phone_number": "555-1234",
        }
        create_response = self.client.post(
            BASE_URL,
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        account_id = create_response.json["id"]  # Fix here
        response = self.client.delete(f"{BASE_URL}/{account_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    unittest.main()
