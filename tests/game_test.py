import json
from rest_framework import status
from rest_framework.test import APITestCase


class GameTests(APITestCase):
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

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # DEFINE GAME TYPE
        url = "/gametypes"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')
        print(response)
        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the name property is correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["skillLevel"], 5)




    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')
        print(response)
        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the name property is correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["maker"], "Milton Bradley")
        self.assertEqual(json_response["skillLevel"], 5)
