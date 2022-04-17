from django.test import TestCase
from api.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import CustomerProfile


class UserManagerTest(TestCase):
    def create_test(self, email, password):
        user = User.objects.create_user(
            email=email, password=password
        )
        return user

    def test_create_staff_user(self):
        test = User.objects.create_staffuser(
            email='exampleOne@gmail.com', password='whaTEver2017'
        )
        self.assertTrue(test.is_active)
        self.assertTrue(test.is_staff)

    def test_create_user(self):
        test = User.objects.create_user(
            email='test@example.com', password='mzta_swift09'
        )
        self.assertEqual(test.email, 'test@example.com')
        self.assertEqual(test.first_name, '')
        self.assertEqual(test.last_name, '')
        self.assertEqual(test.phone_number)
        self.assertTrue(test.is_active)
        self.assertFalse(test.is_staff)
        self.assertFalse(test.is_activated)
        self.assertIsNotNone(test.registration_date)

    def test_create_fulluser(self):
        test = User.objects.create_user(
            email='me@example.com', password='mzta_swift09',
            first_name='John', last_name='Doe', phone_number='0244854227'
        )
        self.assertEqual(test.email, 'me@example.com')
        self.assertEqual(test.first_name, 'John')
        self.assertEqual(test.last_name, 'Doe')
        self.assertEqual(test.phone_number, '0244854227')
        self.assertTrue(test.is_active)
        self.assertFalse(test.is_activated)
        self.assertIsNotNone(test.registration_date)


class RegistrationAPITest(APITestCase):

    def setUp(self):
        self.data_1 = {
            'first_name': 'example',
            'last_name': 'user',
            'email': 'example@gmail.com',
            'phone_number': '0240624914',
            'password': 'password@123'
        }
        self.user_1 = get_user_model().objects.create_user(**self.data_1)
        self.user_1.save()

    def test_successful_account_creation_with_only_email(self):
        """
        test a successful account creation
        with email, password
        """
        data = {
            'email': 'admin@bot.com',
            'password': 'password@123'
        }
        url = reverse('register')
        response = self.client.post(
            path=url,
            data=data
        )
        
        expected_status = status.HTTP_201_CREATED
        self.assertEqual(response.status_code, expected_status)
        expected_data = {
            "is_active": True,
        }
        self.assertEqual(response.data, expected_data)


    def test_account_creation_fail_by_existing_email(self):
        """
        let a creation fail by creating one successful
        user and creating the same user with same
        email than before -> email should be unique
        """
        data = {
            'email': 'example@gmail.com',
            'password': 'password@123'
        }
        url = reverse('register')
        response = self.client.post(
            path=url,
            data=data
        )

        # Testing - response status, response body,
        # created objects at the database
        expected_status = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status)
        expected_data = {
            "error": "User with this email already exist"
        }
        self.assertEqual(response.data, expected_data)

class TestUserInfoModel(TestCase):
    # general user object for the test
    def set_case(self, email, password):
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        return user

    def test_user_info_creation(self):
        self.set_case('user@bot.com', '12345678')
        self.assertIsNotNone(CustomerProfile.user)
