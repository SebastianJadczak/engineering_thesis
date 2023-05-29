from django.db import models


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=40)
    quarter = models.CharField(max_length=40)
    year = models.CharField(max_length=40)


class CategoryProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name_product = models.CharField(max_length=80)
    id_category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    price_product = models.DecimalField(max_digits=7, decimal_places=2)


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=8)


class Sales(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    id_data = models.ForeignKey(Data, on_delete=models.CASCADE)
    id_product = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
