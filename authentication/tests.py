from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def test_login_page_is_available(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connectez-vous')

    def test_signup_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'lectrice',
                'password1': 'MotDePasseTest2026!',
                'password2': 'MotDePasseTest2026!',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(
            get_user_model().objects.filter(username='lectrice').exists()
        )
        self.assertIn('_auth_user_id', self.client.session)

    def test_home_requires_authentication(self):
        response = self.client.get(reverse('home'))

        expected_url = f"{reverse('login')}?next={reverse('home')}"
        self.assertRedirects(response, expected_url)

    def test_logout_ends_session(self):
        user = get_user_model().objects.create_user(
            username='lecteur',
            password='MotDePasseTest2026!',
        )
        self.client.force_login(user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_admin_login_page_is_available(self):
        response = self.client.get(reverse('admin:login'))

        self.assertEqual(response.status_code, 200)
