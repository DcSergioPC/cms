from django.test import TestCase
from cuentas.models import CustomUser

class TestCustomUserModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            age=25,
            password='secret',
            role='admin'
        )

    def test_user_created(self):
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_username(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_email(self):
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_age(self):
        self.assertEqual(self.user.age, 25)

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'testuser@example.com')
