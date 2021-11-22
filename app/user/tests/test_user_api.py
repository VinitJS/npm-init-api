from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """
        Test user public APIs
        > success variations
            - fields conbinations
        > failure variations
            - missing fields
            - incorrect data type
            - incorrect data format
            - access denied
    """

    def setUp(self):
        # before all
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'testPass,123',
            'name': 'Test User Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data);

    def test_try_create_user_exists(self):
        """Test trying to create user that already exists"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'testPass,123'
        }
        create_user(**payload);

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'test'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'Testpass,123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_invalid_credentials(self):
        """Test that a token is not created when invalid credentials are passed"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'Testpass,123'
        }
        create_user(**payload)
        payload['password'] = 'wrong'
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_user(self):
        """Test that a token is not created when user does not exist"""
        payload = {
            'email': 'testuser@npminit.com',
            'password': 'Testpass,123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """Test the email and password are required"""
        payload = {
            'email': 'testuser@npminit.com'
        }
        res = self.client.post(TOKEN_URL, payload)
    
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)