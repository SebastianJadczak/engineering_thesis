from django.db import models


class CategoryProduct(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=30)
    descriptions = models.TextField()
    font_category = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_category(cls):
        return cls.objects.all()

    @classmethod
    def get_category_after_slug(cls,slug):
        return cls.objects.filter(slug=slug)

    @classmethod
    def get_category_after_name(cls, name: str):
        return cls.objects.filter(name=name)

    @classmethod
    def get_id_category_after_slug(cls, slug):
        return cls.objects.filter(slug=slug).first().id

    @classmethod
    def get_name_category_after_id(cls, id):
        return cls.objects.filter(id__in=id).first().name


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

    @classmethod
    def get_highest_rated_products(cls):
        return cls.objects.all().order_by('-average_grade')[:10]

    @classmethod
    def get_all_products(cls):
        return cls.objects.all()

    @classmethod
    def get_product_after_id(cls,id_product: object):
        return cls.objects.filter(id__in=id_product)

    @classmethod
    def get_products_after_name(cls, name_product: str):
        return cls.objects.filter(name_product=name_product)

    @classmethod
    def get_all_products_with_promotion(cls):
        return cls.objects.filter(promotion=True)

    @classmethod
    def get_product_after_category(cls, name):
        return cls.objects.filter(category_product=name)

    @classmethod
    def get_products_with_category_after_slug(cls, slug):
        name = CategoryProduct.get_id_category_after_slug(slug)
        return cls.get_product_after_category(name)
