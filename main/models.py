from django.db import models


class ProductShop(models.Model):
    name = models.CharField(max_length=40)
    descriptions = models.TextField()
    average_grade = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    image_product = models.ImageField(upload_to='media/image_product/%Y/%m%d')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    @staticmethod
    def get_highest_rated_products():
        return ProductShop.objects.all().order_by('-average_grade')[:10]


class CategoryProduct(models.Model):
    name = models.CharField(max_length=40)
    descriptions = models.TextField()
