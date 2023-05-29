from django.shortcuts import render
from django.views import View

from customer_orders.forms.order_form import OrderForm
from customer_orders.models import ElementInCustomerOrder
from main.models import CategoryProduct
from shopping_cart.shopping_cart import ShoppingCart


class CustomerOrder(View):
    template_name = 'create_order.html'
    form = OrderForm()
    category_product = CategoryProduct.get_all_category()

    def get(self, request, *args, **kwargs):
        cart = ShoppingCart(request)
        return render(request, 'create_order.html',
                      {'cart': cart, 'form': self.form, 'category_product': self.category_product})

    def post(self, request):
        form = OrderForm(request.POST)
        cart = ShoppingCart(request)
        if form.is_valid():
            order = form.save()
            for item in cart:
                ElementInCustomerOrder.create_element_in_order(order,
                                                               item['product_shop'],
                                                               item['price'],
                                                               item['amount'])
            cart.clear_shopping_cart()
            return render(request, 'finish.html', {
                'cart': cart, 'form': form, 'category_product': self.category_product
            })
