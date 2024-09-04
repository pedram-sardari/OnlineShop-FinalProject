from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from customers.models import Customer
from orders.models import Order, OrderItem
from products.models import Product, Category, StoreProduct
from vendors.models import Store
from website.constants import UserType


class TestCustomerModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('set_perms')
        cls.customer_group = Group.objects.get(name=UserType.CUSTOMER)

    def setUp(self):
        self.customer = Customer.objects.create(
            email='testuser@example.com',
            phone='09123456789',
            password='password',
            first_name='John',
            last_name='Doe',
            date_of_birth=timezone.datetime(1990, 1, 1),
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.email, 'testuser@example.com')
        self.assertEqual(self.customer.phone, '09123456789')
        self.assertEqual(self.customer.get_full_name(), 'John Doe')
        self.assertEqual(self.customer.get_short_name(), 'testuser')
        self.assertFalse(self.customer.is_staff)
        self.assertFalse(self.customer.is_superuser)
        self.assertIn(self.customer_group, self.customer.groups.all())

    def test_set_group(self):
        self.customer.groups.clear()
        self.customer.set_group()
        self.assertIn(self.customer_group, self.customer.groups.all())

    def test_is_customer(self):
        user = User.objects.get(id=self.customer.id)
        self.assertTrue(Customer.is_customer(user))

    def test_get_customer(self):
        user = User.objects.get(id=self.customer.id)
        self.assertEqual(Customer.get_customer(user), self.customer)

    def test_has_ordered_product(self):
        cat = Category.objects.create(name='cat1')
        product = Product.objects.create(name='product1', category=cat)
        store = Store.objects.create(name='store')
        store_product = StoreProduct.objects.create(product=product, store=store)
        order = Order.objects.create(customer=self.customer, is_paid=True)
        OrderItem.objects.create(order=order, store_product=store_product)
        self.assertTrue(self.customer.has_ordered_product(product))
