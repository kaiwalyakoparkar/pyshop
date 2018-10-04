from django.test import TestCase
from rest_framework import serializers

from pyshop.settings import BASE_DIR
from website.models import Category, Product
from ..serializers import CategorySerializer, ProductSerializer


class CategorySerializerTest(TestCase):
    """ Test case for the Category model serializer """

    def setUp(self):
        self.category = Category(description='Furnitures')
        self.serializer = CategorySerializer(instance=self.category)
        self.json = {
            'description': '',
        }

    def test_description_content(self):
        """ Test description field value """

        self.assertEqual(
            self.category.description,
            self.serializer.data['description']
        )

    def test_blank_description(self):
        """ Test blank description field value """

        serializer = CategorySerializer(data=self.json)

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn('description', serializer.errors.keys())
        self.assertIn('blank', str(serializer.errors.values()))


class ProductSerializerTest(TestCase):
    """ Test case for the Product model serializer """

    def setUp(self):
        self.json = {
            'barcode': '789789789',
            'title': '4654',
            'description': '654',
            'image': '{}/{}'.format(BASE_DIR, 'download.jpg'),
            'price': '123.000',
            'category': 1
        }

        self.category = Category.objects.create(description='Furnitures')

        self.product = Product(
            barcode='789789789',
            title='Mattress',
            description='Sleep Mattress',
            image='{}/{}'.format(BASE_DIR, 'download.jpg'),
            price=123.000,
            category=self.category
        )
        self.serializer = ProductSerializer(
            instance=self.product
        )

    def test_barcode_content(self):
        """ Test barcode field value """

        self.assertEqual(
            self.product.barcode,
            self.serializer.data['barcode']
        )

    def test_title_content(self):
        """ Test title field value """

        self.assertEqual(
            self.product.title,
            self.serializer.data['title']
        )

    def test_description_content(self):
        """ Test description field value """

        self.assertEqual(
            self.product.description,
            self.serializer.data['description']
        )

    def test_price_content(self):
        """ Test price field value """

        self.assertEqual(
            self.product.price,
            float(self.serializer.data['price'])
        )

    def test_category_content(self):
        """ Test category id field value """

        self.assertEqual(
            self.product.category.id,
            self.serializer.data['category']
        )

    def test_null_category(self):
        """ Test using null category id value """

        data = self.json
        data.update({'category': ''})
        exception_serializer = ProductSerializer(data=data)

        with self.assertRaises(serializers.ValidationError):
            exception_serializer.is_valid(raise_exception=True)
        self.assertIn('category', exception_serializer.errors.keys())
        self.assertIn('null', str(exception_serializer.errors.values()))
