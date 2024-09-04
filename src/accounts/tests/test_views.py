from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from customers.models import Customer
from vendors.models import Staff, Store

User = get_user_model()


class EmailLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('set_perms')

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login-email').replace('-us', '')

        self.store = Store.objects.create(name="store1")

        self.customer_user = Customer.objects.create_user(email='customer@g.com', password='password')
        self.staff_user = Staff.objects.create_user(email='staff@g.com', password='password', store=self.store)

    def test_login_get_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/login_email.html')

    def test_login_successful_as_customer(self):
        response = self.client.post(self.login_url, {
            'username': 'customer@g.com',
            'password': 'password',
        }, )
        self.assertRedirects(response, settings.CUSTOMERS_LOGIN_REDIRECT_URL)

    def test_login_successful_as_staff(self):
        response = self.client.post(self.login_url, {
            'username': 'staff@g.com',
            'password': 'password',
        })
        self.assertRedirects(response, settings.STAFF_LOGIN_REDIRECT_URL)

    def test_redirect_logged_in_users(self):
        self.client.force_login(self.customer_user)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('home'))

    def test_redirect_next_url(self):
        url = f"{reverse('accounts:login-email')}?next={reverse('accounts:personal-info-detail')}"
        response = self.client.post(url, {
            'username': 'customer@g.com',
            'password': 'password',
        }, )
        self.assertRedirects(response, reverse('accounts:personal-info-detail'))


class OTPLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('set_perms')

    def setUp(self):
        self.client = Client()
        self.phone_login_url = reverse('accounts:login-phone').replace('-us', '')
        self.phone_login_verify_url = reverse('accounts:login-phone-verify').replace('-us', '')

        self.store = Store.objects.create(name="store1")

        self.customer_user = Customer.objects.create_user(phone='09375491050')
        self.staff_user = Staff.objects.create_user(phone='09375491051', store=self.store)

    def test_login_get_page(self):
        response = self.client.get(self.phone_login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/login_email.html')

    def test_login_successful_as_customer(self):
        response = self.client.post(self.phone_login_url, {'phone': '09375491050'})
        self.assertRedirects(response, self.phone_login_verify_url)

        response = self.client.post(self.phone_login_verify_url, {
            'otp': self.client.session.get('otp')
        })
        self.assertRedirects(response, settings.CUSTOMERS_LOGIN_REDIRECT_URL)

    def test_login_successful_as_staff(self):
        response = self.client.post(self.phone_login_url, {'phone': '09375491051'})
        self.assertRedirects(response, self.phone_login_verify_url)

        response = self.client.post(self.phone_login_verify_url, {
            'otp': self.client.session.get('otp')
        })
        self.assertRedirects(response, settings.STAFF_LOGIN_REDIRECT_URL)

    def test_redirect_logged_in_users(self):
        self.client.force_login(self.customer_user)
        response = self.client.get(self.phone_login_verify_url)
        self.assertRedirects(response, reverse('home'))

    #
    def test_redirect_next_url(self):
        response = self.client.post(self.phone_login_url, {'phone': '09375491050'})
        self.assertRedirects(response, self.phone_login_verify_url)

        url = f"{self.phone_login_verify_url}?next={reverse('accounts:personal-info-detail')}"
        response = self.client.post(url, {
            'otp': self.client.session.get('otp')
        })
        self.assertRedirects(response, reverse('accounts:personal-info-detail'))
