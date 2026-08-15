from django.test import TestCase
from scheduling.models import Client, Appointment
from django.utils import timezone
from datetime import timedelta

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name="Test Client",
            email="test@client.com",
            phone="11999999999",
            instagram_handle="@testclient"
        )
        self.appointment = Appointment.objects.create(
            client=self.client,
            date_time=timezone.now() + timedelta(days=1),
            description="Tatuagem de teste",
            status="PENDING",
            estimated_price=250.00
        )

    def test_client_creation(self):
        self.assertEqual(self.client.name, "Test Client")

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.client.name, "Test Client")
        self.assertEqual(self.appointment.status, "PENDING")
        self.assertTrue(self.appointment.date_time > timezone.now())

    def test_appointment_string_representation(self):
        expected_str = f"{self.client.name} - {self.appointment.date_time.strftime('%d/%m/%Y %H:%M')}"
        self.assertEqual(str(self.appointment), expected_str)
