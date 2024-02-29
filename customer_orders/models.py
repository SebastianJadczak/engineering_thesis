from django.db import models

from main.models import ProductShop


class CustomerOrder(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    paid_to = models.BooleanField(default=False)
    customer_first_name = models.CharField(max_length=80)
    customer_last_name = models.CharField(max_length=80)
    email = models.EmailField()
    address = models.CharField(max_length=270)
    zip_code = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return 'Zamówienie z dnia {} nr {} w mieście {}'.format(self.create_date, self.id, self.location)

    @classmethod
    def get_all_orders(cls):
        return cls.objects.all()

    @classmethod
    def get_all_not_archived_orders(cls):
        return cls.objects.filter(archived=False)


class ElementInCustomerOrder(models.Model):
    customer_order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductShop, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    price_product = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return 'Produkt: {}'.format(self.id)

    @classmethod
    def get_all_element_in_order(cls, order: int):
        return cls.objects.filter(customer_order=order)

    @classmethod
    def create_element_in_order(cls,customer_order, product, price_product, amount):
        return cls.objects.create(customer_order=customer_order,
                                                     product=product,
                                                     amount=amount,
                                                     price_product=price_product)

    def take_total_cost_this_product(self):
        cost = self.price_product * self.amount
        return cost
