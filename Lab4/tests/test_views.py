from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from Lab4.models import Product, Customer, Order
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class ProductApiTest(APITestCase):
  def setUp(self):
    self.product = Product.objects.create(
      name='Temporary product',
      price=1.99,
      available=True
    )
    self.product_list_url = reverse('product-list')
    self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
    self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
    self.admin = User.objects.create_superuser(username='testadmin', password='testpassword')
    self.client = APIClient()

  def test_get_all_products_as_regular_user(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.get(self.product_list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['name'], 'Temporary product')
    self.assertEqual(response.data[0]['price'], '1.99')
    self.assertTrue(response.data[0]['available'])

  def test_get_all_products_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.get(self.product_list_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['name'], 'Temporary product')
    self.assertEqual(response.data[0]['price'], '1.99')
    self.assertTrue(response.data[0]['available'])

  def test_get_single_product_as_regular_user(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.get(self.product_detail_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'Temporary product')
    self.assertEqual(response.data['price'], '1.99')
    self.assertTrue(response.data['available'])

  def test_get_single_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.get(self.product_detail_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'Temporary product')
    self.assertEqual(response.data['price'], '1.99')
    self.assertTrue(response.data['available'])

  def test_create_new_product_as_regular_user(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
    response = self.client.post(self.product_list_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_create_new_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "Temporary Product 2", "price": 4.99, "available": True}
    response = self.client.post(self.product_list_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], 'Temporary Product 2')
    self.assertEqual(response.data['price'], '4.99')
    self.assertTrue(response.data['available'])

  def test_update_product_as_regular_user(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "Modified Product", "price": 1.99, "available": True}
    response = self.client.put(self.product_detail_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_update_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "Modified Product", "price": 1.99, "available": True}
    response = self.client.put(self.product_detail_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], 'Modified Product')
    self.assertEqual(response.data['price'], '1.99')
    self.assertTrue(response.data['available'])

  def test_delete_product_as_regular_user(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.delete(self.product_detail_url)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_delete_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    response = self.client.delete(self.product_detail_url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Product.objects.count(), 0)
  
  def test_create_product_with_invalid_data_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "", "price": -1, "available": True}
    response = self.client.post(self.product_list_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_product_with_invalid_data_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    data = {"name": "", "price": -1, "available": True}
    response = self.client.put(self.product_detail_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_get_nonexistent_product(self):
    self.token = str(AccessToken.for_user(self.regular_user))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    nonexistent_product_url = reverse('product-detail', kwargs={'pk': 999})
    response = self.client.get(nonexistent_product_url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_update_nonexistent_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    nonexistent_product_url = reverse('product-detail', kwargs={'pk': 999})
    data = {"name": "Nonexistent Product", "price": 1.99, "available": True}
    response = self.client.put(nonexistent_product_url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  def test_delete_nonexistent_product_as_admin(self):
    self.token = str(AccessToken.for_user(self.admin))
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    nonexistent_product_url = reverse('product-detail', kwargs={'pk': 999})
    response = self.client.delete(nonexistent_product_url)
    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

