from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from main.models import ProductShop, CategoryProduct
from shopping_cart.forms.forms import AmountProductInCart
from shopping_cart.shopping_cart import ShoppingCart


class Cart(View):
    category_product = CategoryProduct.get_all_category()

    def post(self, request, product_id):
        cart = ShoppingCart(request)
        product = get_object_or_404(ProductShop, id=product_id)
        form = AmountProductInCart(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add_product_to_shopping_cart(product, cd['amount'], cd['update'])
        else:
            print('error')
        return redirect('shopping_cart:shopping_cart_detail')

    def get(self, request, *args, **kwargs):
        cart = ShoppingCart(request)
        for item in cart:
            item['update_amount_form'] = AmountProductInCart(initial={'amount': item['amount'], 'update': True})
        return render(request, 'cart/detail.html', {'cart': cart, 'category_product': self.category_product})

    def cart_remove(request, product_id):
        cart = ShoppingCart(request)
        product = get_object_or_404(ProductShop, id=product_id)
        cart.remove_product_with_shopping_cart(product)
        return HttpResponseRedirect(reverse('shopping_cart:shopping_cart_detail'))
