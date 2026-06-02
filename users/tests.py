from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


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
