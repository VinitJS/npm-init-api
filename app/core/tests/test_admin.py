from django.test import TestCase, \
                        Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        semail = 'super@npminit.com'
        spassword = 'SuperPass,123'
        self.admin_user = get_user_model().objects.create_superuser(semail, spassword)
        self.client.force_login(self.admin_user)
        email = 'test@npminit.com'
        password = 'TestPass,123'
        name = 'Test User'
        self.user = get_user_model().objects.create_user(email, password, name=name)

    def test_users_listed(self):
        """Test users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        status_code = 200
        self.assertEqual(res.status_code, status_code)
    
    def test_create_user_pagr(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        status_code = 200
        self.assertEqual(res.status_code, status_code)