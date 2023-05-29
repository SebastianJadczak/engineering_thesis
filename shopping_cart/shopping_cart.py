from decimal import Decimal
from typing import Any

from django.conf import settings

from main.models import ProductShop


class ShoppingCart(object):
    def __init__(self, request):
        self.session = request.session
        self.shopping_cart = self.__get_shopping_cart(self.session)

    def __iter__(self):
        ids_of_products_with_db = self.shopping_cart.keys()
        products_with_db = ProductShop.get_product_after_id(ids_of_products_with_db)

        cart = self.shopping_cart.copy()
        for product in products_with_db:
            cart[str(product.id)]['product_shop'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['amount']
            yield item

    def __len__(self):
        return sum(item['amount'] for item in self.shopping_cart.values())

    def get_price_all_elements_in_shopping_cart(self):
        return sum(Decimal(item['price']) * item['amount'] for item in self.shopping_cart.values())

    def add_product_to_shopping_cart(self, product_shop: Any, amount: int = 1, update_quantity: bool = False):
        id_of_product = str(product_shop.id)
        if id_of_product not in self.shopping_cart:
            self.__set_object_product_in_session_shopping_cart(
                id_of_product=id_of_product,
                product_shop=product_shop
            )
        if update_quantity:
            self.__set_amount_product_in_shopping_cart(
                id_of_product=id_of_product,
                amount=amount
            )
        else:
            self.__update_amount_product_in_shopping_cart(
                id_of_product=id_of_product,
                amount=amount
            )
        self.__save_shopping_cart()

    def remove_product_with_shopping_cart(self, product_shop):
        id_of_product = str(product_shop.id)
        if id_of_product in self.shopping_cart:
            del self.shopping_cart[id_of_product]
            self.__save_shopping_cart()

    def clear_shopping_cart(self):
        del self.session[settings.SHOPPING_CART_SESSION_ID]
        self.__save_shopping_cart()

    def __save_shopping_cart(self):
        self.session.modified = True

    def __set_object_product_in_session_shopping_cart(self, *, id_of_product: str, product_shop: Any):
        self.shopping_cart[id_of_product] = {'amount': 0, 'price': str(product_shop.price)}

    def __set_amount_product_in_shopping_cart(self, *, id_of_product: str, amount: int):
        self.shopping_cart[id_of_product]['amount'] = amount

    def __update_amount_product_in_shopping_cart(self, *, id_of_product: str, amount: int):
        self.shopping_cart[id_of_product]['amount'] += amount

    def __get_shopping_cart(self, session_cart):
        shopping_cart = session_cart.get(settings.SHOPPING_CART_SESSION_ID)
        if not shopping_cart:
            shopping_cart = session_cart[settings.SHOPPING_CART_SESSION_ID] = {}
        return shopping_cart
