from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class RegistrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('register-list')
        cls.existing_user_email = 'existing@example.com'
        cls.password = 'StrongPassword123'
        cls.user = get_user_model().objects.create_user(
            email=cls.existing_user_email,
            username='existinguser',
            phone_number='1234567890',
            password=cls.password,
        )

    def setUp(self):
        self.client = APIClient()

    def test_successful_registration_with_valid_data(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'phone_number': '5558887777',
            'password': self.password,
            'password2': self.password,
            'first_name': 'New',
            'last_name': 'User',
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(email=data['email']).exists())

    def test_registration_fails_if_email_already_exists(self):
        data = {
            'email': self.existing_user_email,
            'username': 'anotheruser',
            'phone_number': '5559990000',
            'password': self.password,
            'password2': self.password,
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(get_user_model().objects.filter(email=self.existing_user_email).count(), 1)

    def test_registration_fails_if_password_is_missing(self):
        data = {
            'email': 'nopassword@example.com',
            'username': 'nopassworduser',
            'phone_number': '5550001111',
            'password2': self.password,
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(get_user_model().objects.filter(email=data['email']).exists())

    def test_registration_fails_if_email_is_missing(self):
        data = {
            'username': 'noemailuser',
            'phone_number': '5550002222',
            'password': self.password,
            'password2': self.password,
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_fails_if_username_is_missing(self):
        data = {
            'email': 'nousername@example.com',
            'phone_number': '5550003333',
            'password': self.password,
            'password2': self.password,
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)


class AuthenticationTests(APITestCase):
    login_url = '/api/token/'
    protected_url = '/products/'

    @classmethod
    def setUpTestData(cls):
        cls.email = 'testuser@example.com'
        cls.password = 'StrongPassword123'
        cls.user = get_user_model().objects.create_user(
            email=cls.email,
            username='testuser',
            phone_number='1234567890',
            password=cls.password,
        )

    def setUp(self):
        self.client = APIClient()

    def test_login_with_invalid_credentials_returns_error(self):
        response = self.client.post(
            self.login_url,
            {'email': 'invalid@example.com', 'password': 'wrongpass'},
            format='json',
        )

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED],
        )
        self.assertTrue(
            response.data,
            'Expected an error response body when login credentials are invalid.',
        )

    def test_successful_login_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            self.login_url,
            {'email': self.email, 'password': self.password},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_protected_endpoint_with_valid_access_token_succeeds(self):
        login_response = self.client.post(
            self.login_url,
            {'email': self.email, 'password': self.password},
            format='json',
        )
        access_token = login_response.data.get('access')

        self.assertIsNotNone(access_token, 'Expected access token in login response.')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoint_without_token_is_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
