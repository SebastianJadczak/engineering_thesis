from django.db import models


class CategoryProduct(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=30)
    descriptions = models.TextField()
    font_category = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_category():
        return CategoryProduct.objects.all()

    @staticmethod
    def get_category_after_slug(slug):
        return CategoryProduct.objects.filter(slug=slug)

    @staticmethod
    def get_category_after_name(name: str):
        return CategoryProduct.objects.filter(name=name)

    @staticmethod
    def get_id_category_after_slug(slug):
        return CategoryProduct.objects.filter(slug=slug).first().id

    @staticmethod
    def get_name_category_after_id(id):
        return CategoryProduct.objects.filter(id__in=id).first().name


class ProductShop(models.Model):
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=40, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    descriptions = models.TextField()
    average_grade = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    image_product = models.ImageField(upload_to='media/image_product/%Y/%m%d')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    promotion = models.BooleanField(default=False)
    available_product = models.BooleanField(default=True)

    class Meta:
        index_together = ('id', 'slug')

    def __str__(self):
        return self.name_product

    @staticmethod
    def get_highest_rated_products():
        return ProductShop.objects.all().order_by('-average_grade')[:10]

    @staticmethod
    def get_all_products():
        return ProductShop.objects.all()

    @staticmethod
    def get_product_after_id(id_product: object):
        return ProductShop.objects.filter(id__in=id_product)

    @staticmethod
    def get_products_after_name(name_product: str):
        return ProductShop.objects.filter(name_product=name_product)

    @staticmethod
    def get_all_products_with_promotion():
        return ProductShop.objects.filter(promotion=True)

    @staticmethod
    def get_product_after_category(name):
        return ProductShop.objects.filter(category_product=name)

    @staticmethod
    def get_products_with_category_after_slug(slug):
        name = CategoryProduct.get_id_category_after_slug(slug)
        return ProductShop.get_product_after_category(name)
