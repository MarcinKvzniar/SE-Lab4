from django.test import TestCase
from Lab4.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
  def test_create_product_with_valid_data(self):
    temp_product = Product.objects.create(
      name='Temporary product',
      price=1.99,
      available=True
    )
    self.assertEqual(temp_product.name, 'Temporary product')
    self.assertEqual(temp_product.price, 1.99)
    self.assertTrue(temp_product.available)
  
  def test_create_product_with_negative_price(self):
    with self.assertRaises(ValidationError):
      temp_product = Product.objects.create(
        name='Invalid product',
        price=-1.99,
        available=True
      )
      temp_product.full_clean()
  
  def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            product = Product(name='', price=1.99, available=True)
            product.full_clean()

  def test_create_product_with_missing_price(self):
      with self.assertRaises(ValidationError):
          product = Product(name='Product without price', price=0, available=True)
          product.full_clean()

  def test_create_product_with_missing_available(self):
      with self.assertRaises(ValidationError):
          product = Product(name='Product without availability', price=1.99, available=None)
          product.full_clean()

  def test_create_product_with_edge_name_length(self):
      max_length_name = 'a' * 255
      temp_product = Product.objects.create(
          name=max_length_name,
          price=1.99,
          available=True
      )
      self.assertEqual(temp_product.name, max_length_name)

      with self.assertRaises(ValidationError):
          product = Product(name='a' * 256, price=1.99, available=True)
          product.full_clean()

  def test_create_product_with_edge_price_value(self):
      min_price_product = Product.objects.create(
          name='Min price product',
          price=0.01,
          available=True
      )
      self.assertEqual(min_price_product.price, 0.01)

      max_price_product = Product.objects.create(
          name='Max price product',
          price=99999999.99,
          available=True
      )
      self.assertEqual(max_price_product.price, 99999999.99)

  def test_create_product_with_invalid_price_format(self):
      with self.assertRaises(ValidationError):
          product = Product(name='Invalid price format', price=1.999, available=True)
          product.full_clean()

class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(
            name='John Doe',
            address='123 Main St'
        )
        self.assertEqual(temp_customer.name, 'John Doe')
        self.assertEqual(temp_customer.address, '123 Main St')

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='', address='123 Main St')
            customer.full_clean()

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe', address='')
            customer.full_clean()

    def test_create_customer_with_edge_name_length(self):
        max_length_name = 'a' * 100
        temp_customer = Customer.objects.create(
            name=max_length_name,
            address='123 Main St'
        )
        self.assertEqual(temp_customer.name, max_length_name)

        with self.assertRaises(ValidationError):
            customer = Customer(name='a' * 101, address='123 Main St')
            customer.full_clean()

    def test_create_customer_with_edge_address_length(self):
        max_length_address = 'a' * 255
        temp_customer = Customer.objects.create(
            name='John Doe',
            address=max_length_address
        )
        self.assertEqual(temp_customer.address, max_length_address)

        with self.assertRaises(ValidationError):
            customer = Customer(name='John Doe', address='a' * 256)
            customer.full_clean()

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe',
            address='123 Main St'
        )
        self.product1 = Product.objects.create(
            name='Product 1',
            price=19.99,
            available=True
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            price=29.99,
            available=False
        )

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'New')
        self.assertIn(self.product1, order.products.all())
        self.assertIn(self.product2, order.products.all())

    def test_create_order_with_missing_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(status='New')
            order.full_clean()

    def test_create_order_with_missing_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer)
            order.full_clean()

    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status='Invalid Status')
            order.full_clean()

    def test_total_price_with_valid_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        self.assertEqual(float(order.total_price()), 49.98)

    def test_total_price_with_no_products(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        self.assertEqual(order.total_price(), 0)

    def test_can_be_fulfilled_with_all_products_available(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1)
        self.assertTrue(order.can_be_fulfilled())

    def test_can_be_fulfilled_with_some_products_unavailable(self):
        order = Order.objects.create(
            customer=self.customer,
            status='New'
        )
        order.products.add(self.product1, self.product2)
        self.assertFalse(order.can_be_fulfilled())
    