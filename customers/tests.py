from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer

class CustomerAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'un client pour les tests de lecture, mise à jour, et suppression
        cls.customer = Customer.objects.create(name="John Doe", email="john@example.com", address="1234 Street")

    def test_create_customer(self):
        """
        Assurez-vous que nous pouvons créer un nouveau client.
        """
        url = reverse('customers:customer-list')
        data = {'name': 'Jane Doe', 'email': 'jane@example.com', 'address': '5678 Drive'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(id=response.data['id']).name, 'Jane Doe')

    def test_list_customers(self):
        """
        Tester la récupération de la liste des clients.
        """
        url = reverse('customers:customer-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_customer(self):
        """
        Tester la récupération d'un client spécifique.
        """
        url = reverse('customers:customer-detail', args=[self.customer.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_update_customer(self):
        """
        Tester la mise à jour d'un client.
        """
        url = reverse('customers:customer-detail', args=[self.customer.id])
        data = {'name': 'John Updated', 'email': 'johnupdated@example.com', 'address': '1234 Street Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'John Updated')

    def test_delete_customer(self):
        """
        Tester la suppression d'un client.
        """
        url = reverse('customers:customer-detail', args=[self.customer.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_invalid_data_create(self):
        """
        Tester la création d'un client avec des données invalides (e.g., email manquant).
        """
        url = reverse('customers:customer-list')
        data = {'name': 'Invalid User', 'address': 'No Email Street'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
