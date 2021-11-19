from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successfully(self):
        """Test creating a new user with an email is successful"""
        email = 'test@npminit.com'
        password = 'TestPass,123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test new user email is normalized"""
        email = 'test@NPMINIT.COM'
        password = 'TestPass,123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_email_invalid(self):
        """Test new user email is invalid"""
        with self.assertRaises(ValueError):
            email = None
            password = 'TestPass,123'
            user = get_user_model().objects.create_user(email, password)

    def test_create_superuser_successfully(self):
        """Test create superuser successfully"""
        email = 'super@npminit.com'
        password = 'SuperPass,123'
        superuser = get_user_model().objects.create_superuser(email, password)
        
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)