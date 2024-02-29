from django.shortcuts import redirect
from django.views.generic import ListView
from customer_orders.models import CustomerOrder, ElementInCustomerOrder
from dashboard.data_warehouse import DataWarehouse
from dashboard.models import Sales
from main.models import CategoryProduct


class DashboardView(ListView):
    template_name = 'dashboard.html'

    model = CategoryProduct
    orders = CustomerOrder.get_all_orders()

    def post(self, request):
        not_archived = [self.__create_object_order(order, archived=True) for order in
                        CustomerOrder.get_all_not_archived_orders()]

        [self.__archive_data(element) for element in not_archived]
        return redirect('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_orders'] = self.__get_list_orders()
        return context

    def __count_the_order_amount(self, elements):
        total_price = 0
        for element in elements:
            total_price = element.price_product * element.amount
        return total_price

    def __create_object_order(self, order, archived=False):
        elements = ElementInCustomerOrder.get_all_element_in_order(order.id)
        total_price = self.__count_the_order_amount(elements)
        obj = {
            "id": order.id,
            "create_date_day": f'{order.create_date.date().day}',
            "create_date_month": f'{order.create_date.date().month}',
            "create_date_year": f'{order.create_date.date().year}',
            "name_customer": order.customer_first_name,
            "customer_last_name": order.customer_last_name,
            "zip_code": order.zip_code,
            "archived": order.archived,
            "products": elements,
            "total_price": total_price
        }
        if archived:
            el = CustomerOrder.objects.filter(id=order.id).first()
            el.archived = True
            el.save()
        return obj

    def __get_list_orders(self):
        orders = [self.__create_object_order(order) for order in self.orders]
        return orders

    def __archive_data(self, element):
        try:
            DataWarehouse.create_sales(
                id_data=DataWarehouse.create_data_object(element),
                id_product=DataWarehouse.create_product_with_category(element),
                id_client=DataWarehouse.create_client(element),
                total_price=element['total_price']
            )
        except:
            print('Coś poszło nie tak, obiekt nie został stworzony')


class FirstDimensionDashboard(ListView):
    template_name = 'first_dashboard.html'
    model = Sales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_orders'] = self.__get_sales_after_year()
        return context

    def __get_elements_only_this_year(self, el):
        if el.id_data.year == '2023':
            return el

    def __get_sales_after_year(self):
        list_elements = [self.__get_elements_only_this_year(el) for el in self.model.objects.all()]
        return list_elements


class SecondDimensionDashboard(ListView):
    template_name = 'second_dashboard.html'
    model = Sales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_orders'] = self.__get_sales_after_second_quarter()
        return context

    def __get_elements_after_zip_code(self, el):
        if el.id_client.zip_code == '12-1234':
            return el

    def __get_sales_after_second_quarter(self):
        list_elements = [self.__get_elements_after_zip_code(el) for el in self.model.objects.all()]
        return list_elements


class ThirdDimensionDashboard(ListView):
    template_name = 'third_dashboard.html'
    model = Sales

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_orders'] = self.__get_sales_after_total_price()
        return context

    def __get_elements_only_larger_than_three_thousand_zlotys(self, el):
        if el.total_price > 100:
            return el

    def __get_sales_after_total_price(self):
        list_elements = [self.__get_elements_only_larger_than_three_thousand_zlotys(el) for el in
                         self.model.objects.all()]
        return list_elements
