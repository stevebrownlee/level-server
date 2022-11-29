import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType


# pylint: disable=no-member
class GameTypeTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

    def test_create_game_type(self):
        """
        Ensure we cannot create a new game type.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "label": "Space games"
        }

        # Initiate request and store response
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_game_type(self):
        """
        Ensure we can delete an non-existent game type.
        """

        # Use the API to delete an invalid game type
        response = self.client.delete(f"/gametypes/34556")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_fake_game_type(self):
        """
        Ensure we can get an existing game type.
        """
        game_type = GameType()
        game_type.label = "Farfegnugën"
        game_type.save()

        response = self.client.get(f"/gametypes/{game_type.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], game_type.id)
        self.assertEqual(json_response["label"], "Farfegnugën")
