from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from accounts.models import User, UserAddress


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="09123456789",
            password="Aa@123456",
            national_id="1234567890",
            date_of_birth=timezone.datetime(1990, 1, 1),
            gender=User.Gender.MALE,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.phone, "09123456789")
        self.assertEqual(self.user.national_id, "1234567890")
        self.assertEqual(self.user.gender, User.Gender.MALE)
        self.assertTrue(self.user.check_password('Aa@123456'))

    def test_email_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                first_name="Jane",
                last_name="Doe",
                email="john.doe@example.com",
                phone="09123456780",
            )

    def test_phone_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                first_name="Jane",
                last_name="Doe",
                email="jane.doe@example.com",
                phone="09123456789",
                national_id="0987654321",
            )

    def test_national_id_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                first_name="Jane",
                last_name="Doe",
                email="jane.doe@example.com",
                phone="09123456780",
                national_id="1234567890",
            )

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "John Doe")

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "john.doe")

    def test_is_customer_property(self):
        self.assertTrue(self.user.is_customer)
        self.user.is_staff = True
        self.user.save()
        self.assertFalse(self.user.is_customer)

    def test_age_property(self):
        self.assertEqual(self.user.age, 34)

        # Test with date_of_birth being None
        self.user.date_of_birth = None
        self.assertIsNone(self.user.age)

    def test_save_method(self):
        user = User(first_name="Test", last_name="User", email="", phone="")
        with self.assertRaises(ValueError):
            user.save()

    def test_soft_delete_method(self):
        self.user.delete(soft_delete=True)
        self.assertTrue(self.user.is_deleted)
        self.assertTrue(User.objects.all_objects().filter(id=self.user.id, is_deleted=True).exists())

    def test_hard_delete(self):
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_profile_image_upload_to(self):
        filename = "profile.jpg"
        path = self.user.profile_image_upload_to(filename)
        self.assertEqual(path, f"user_images/{filename}")

    def test_get_default_user_address(self):
        address1 = UserAddress.objects.create(user=self.user, province="tehran", city='tehran', is_default=False)
        address2 = UserAddress.objects.create(user=self.user, province="yazd", city='yazd', is_default=True)
        self.assertEqual(self.user.get_default_user_address(), address2)

        # No default should return the first one
        address2.is_default = False
        address2.save()
        self.assertEqual(self.user.get_default_user_address(), address1)
