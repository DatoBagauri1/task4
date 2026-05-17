import random
import uuid

from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Product, ProductTag

fake = Faker()

class Command(BaseCommand):
    help = "Create 1000 random products"

    def handle(self, *args, **kwargs):
        currencies = ['GEL', 'USD', 'EUR']

        tag_names = [
            "Electronics",
            "Fashion",
            "Home",
            "Sports",
            "Books",
            "Beauty",
            "Toys",
            "Food",
        ]

        tags = []

        for name in tag_names:
            tag, _ = ProductTag.objects.get_or_create(name=name)
            tags.append(tag)

        products = []

        for _ in range(1000):
            product = Product.objects.create(
                name=f"{fake.word().capitalize()}-{uuid.uuid4().hex[:8]}",
                description=fake.text(max_nb_chars=200),
                price=round(random.uniform(5, 5000), 2),
                currency=random.choice(currencies),
            )

            random_tags = random.sample(tags, random.randint(1, 3))
            product.tags.set(random_tags)

            products.append(product)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(products)} products"
            )
        )