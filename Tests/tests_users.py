from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password
from users.models import User
from tasks.models import Task

class UserViewsTests(TestCase):
    def setUp(self):
        """
        Set up test data before each test.
        """
        # Create a manager user
        self.manager = User.objects.create(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            role="manager",
            password=make_password("managerpassword")  # Hashed password
        )

        # Create an employee user
        self.employee = User.objects.create(
            first_name="Employee",
            last_name="User",
            email="employee@example.com",
            role="employee",
            password=make_password("employeepassword")  # Hashed password
        )

        # Set up the test client
        self.client = Client()

    def test_login_view(self):
        """
        Test the login view.
        """
        # Test successful login for manager
        response = self.client.post(reverse('users:login'), {
            'email': 'manager@example.com',
            'password': 'managerpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirection
        self.assertRedirects(response, reverse('tasks:manager_tasks'))  # Check redirection to manager tasks page

        # Test successful login for employee
        response = self.client.post(reverse('users:login'), {
            'email': 'employee@example.com',
            'password': 'employeepassword'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirection
        self.assertRedirects(response, reverse('tasks:employee_tasks'))  # Check redirection to employee tasks page

        # Test invalid password
        response = self.client.post(reverse('users:login'), {
            'email': 'manager@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check that the page reloads
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid password')  # Check error message

        # Test non-existent user
        response = self.client.post(reverse('users:login'), {
            'email': 'nonexistent@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)  # Check that the page reloads
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'User not found')  # Check error message

    def test_register_view(self):
        """
        Test the register view.
        """
        # Test successful registration
        response = self.client.post(reverse('users:register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'birthday': '1990-01-01',
            'role': 'employee',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirection
        self.assertRedirects(response, reverse('users:login'))  # Check redirection to login page
        self.assertTrue(User.objects.filter(email='john@example.com').exists())  # Check that the user was created

        # Test password mismatch
        response = self.client.post(reverse('users:register'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'phone_number': '0987654321',
            'birthday': '1995-01-01',
            'role': 'employee',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check that the page reloads
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Passwords do not match')  # Check error message

        # Test email already exists
        response = self.client.post(reverse('users:register'), {
            'first_name': 'Manager',
            'last_name': 'User',
            'email': 'manager@example.com',  # Existing email
            'phone_number': '1234567890',
            'birthday': '1990-01-01',
            'role': 'manager',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Check that the page reloads
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Email already exists')  # Check error message