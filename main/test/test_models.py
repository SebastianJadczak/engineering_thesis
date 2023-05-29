from django.test import TestCase
from main.models import CategoryProduct, ProductShop


class MainApplicationModelTestCase(TestCase):
    """Klasa odpowiedzialna za testy dla modelów w aplikacji main."""

    def setUp(self):
        """Zdefiniowanie obiektu na podstawie modelu."""
        self.category = CategoryProduct.objects.create(
            name='Pralki',
            slug='Pralki',
            descriptions='Przykładowy opis',
            font_category='fa-regular fa-washing-machine'
        )
        self.product = ProductShop.objects.create(
            category_product=self.category,
            name_product="Przykładowy",
            slug="Przykładowy",
            descriptions="Przykładowy opis",
            average_grade=3,
            image_product=None,
            price=1.23,
            promotion=True,
            available_product=True
        )

    def test_set_CategoryProduct(self):
        """Test tworzenia i zapisu obiektu w bazie."""
        self.assertIsNotNone(self.category.id)

    def test_get_all_category_method(self):
        self.assertIsNotNone(CategoryProduct.get_all_category())

    def test_get_category_after_slug_method(self):
        self.assertIsNotNone(CategoryProduct.get_category_after_slug('Pralki'))

    def test_get_category_after_name_method(self):
        self.assertIsNotNone(CategoryProduct.get_category_after_name('Pralki'))

    def test_get_id_category_after_slug_method(self):
        self.assertIsNotNone(CategoryProduct.get_id_category_after_slug('Pralki'))

    def test_get_name_category_after_id_method(self):
        self.assertIsNotNone(CategoryProduct.get_name_category_after_id([self.category.id]))

    def test_set_ProductShop(self):
        """Test tworzenia i zapisu obiektu w bazie."""
        self.assertIsNotNone(self.product.id)

    def test_get_all_products_method(self):
        self.assertIsNotNone(ProductShop.get_all_products())

    def test_get_product_after_id_method(self):
        self.assertIsNotNone(ProductShop.get_product_after_id([self.product.id]))

    def test_get_products_after_name_method(self):
        self.assertIsNotNone(ProductShop.get_products_after_name(self.product.name_product))

    def test_get_all_products_with_promotion_method(self):
        self.assertIsNotNone(ProductShop.get_all_products_with_promotion())

    def test_get_product_after_category_method(self):
        self.assertIsNotNone(ProductShop.get_product_after_category(self.category))

    def test_get_products_with_category_after_slug_method(self):
        self.assertIsNotNone(ProductShop.get_products_with_category_after_slug(self.category.slug))
