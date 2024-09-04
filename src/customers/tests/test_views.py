from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from customers.models import Customer

User = get_user_model()


class CustomerRegisterByEmailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('set_perms')

    def setUp(self):
        self.client = Client()
        self.register_by_email_url = reverse('customers:register-by-email').replace('-us', '')
        self.username = 'customer@g.com'
        self.password = 'Aa@123456'

    def test_register_successful(self):
        response = self.client.post(self.register_by_email_url, {
            'email': self.username,
            'password1': self.password,
            'password2': self.password,
        }, )
        qs = Customer.objects.filter(email=self.username)
        self.assertEqual(qs.count(), 1)
        self.assertTrue(qs.first().check_password(self.password))
        self.assertRedirects(response, reverse('accounts:personal-info-detail'))


class CustomerRegisterByPhoneTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('set_perms')

    def setUp(self):
        self.client = Client()
        self.register_by_phone_url = reverse('customers:register-by-phone').replace('-us', '')
        self.register_by_phone_verify_url = reverse('customers:register-by-phone-verify').replace('-us', '')
        self.phone = '09375491010'

    def test_register_successful(self):
        response = self.client.post(self.register_by_phone_url, {
            'phone': self.phone
        })
        self.assertRedirects(response, reverse('customers:register-by-phone-verify'))

        response = self.client.post(self.register_by_phone_verify_url, {
            'otp': self.client.session.get('otp')
        })
        qs = Customer.objects.filter(phone=self.phone)
        self.assertEqual(qs.count(), 1)
        self.assertRedirects(response, reverse('accounts:personal-info-detail'))
