from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Product, Review


class ProductModelTests(TestCase):
    def test_product_created_successfully_with_valid_data(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=25.5,
            currency='USD',
        )

        self.assertIsNotNone(product.pk)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, 25.5)
        self.assertEqual(product.currency, 'USD')

    def test_product_name_is_saved_correctly(self):
        product = Product.objects.create(
            name='Saved Name',
            description='Another description',
            price=15.0,
            currency='EUR',
        )

        self.assertEqual(str(product), 'Saved Name')

    def test_product_price_is_saved_correctly(self):
        product = Product.objects.create(
            name='Price Test',
            description='Price description',
            price=99.99,
            currency='GEL',
        )

        self.assertEqual(product.price, 99.99)

    def test_product_currency_is_saved_correctly(self):
        product = Product.objects.create(
            name='Currency Test',
            description='Currency description',
            price=12.0,
            currency='GEL',
        )

        self.assertEqual(product.currency, 'GEL')

    def test_product_str_returns_expected_value(self):
        product = Product.objects.create(
            name='Display Name',
            description='Display description',
            price=40.0,
            currency='USD',
        )

        self.assertEqual(str(product), 'Display Name')

    def test_invalid_product_data_is_rejected(self):
        product = Product(
            name='Invalid Product',
            description='Description',
            price=50.0,
            currency='GBP',
        )

        with self.assertRaises(ValidationError):
            product.full_clean()


class ReviewModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='reviewer@example.com',
            username='reviewer',
            phone_number='5556667777',
            password='StrongPassword123',
        )
        cls.product = Product.objects.create(
            name='Review Product',
            description='Review description',
            price=20.0,
            currency='USD',
        )

    def test_review_created_successfully_with_valid_data(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='Great product',
            rating=5,
        )

        self.assertIsNotNone(review.pk)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.content, 'Great product')
        self.assertEqual(review.rating, 5)

    def test_rating_cannot_exceed_allowed_maximum(self):
        review = Review(
            product=self.product,
            user=self.user,
            content='Too high rating',
            rating=6,
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_can_exist_without_user_if_model_allows_nullable_user(self):
        review = Review.objects.create(
            product=self.product,
            content='Anonymous review',
            rating=4,
        )

        self.assertIsNone(review.user)
        self.assertEqual(review.rating, 4)

    def test_deleting_product_deletes_related_reviews(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='Cascade review',
            rating=3,
        )

        self.product.delete()

        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_deleting_user_sets_review_user_to_none(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='User deleted review',
            rating=2,
        )

        self.user.delete()
        review.refresh_from_db()

        self.assertIsNone(review.user)
