import math
from dashboard.models import Data, Product, Client, Sales
from dashboard.models import CategoryProduct as CategoryProductDashboard


class DataWarehouse:

    @staticmethod
    def create_data_object(element):
        print('create_data_object')
        data = Data(month=element['create_date_month'],
                    quarter=math.ceil(int(element['create_date_month']) / 3.),
                    year=element['create_date_year']
                    )
        data.save()
        return data

    @staticmethod
    def create_product_with_category(element):
        print('create_product_with_category')
        return_product_array = []
        for prod in element['products']:
            if not CategoryProductDashboard.objects.filter(name=prod.product.category_product):
                print("brak")
                cat_prod = CategoryProductDashboard(name=prod.product.category_product)
                cat_prod.save()
                print(cat_prod.id)
                # tworzenie produktu
                product_dashboard = Product(
                    id_category_product=cat_prod,
                    name_product=prod.product.name_product,
                    amount=prod.amount,
                    price_product=prod.price_product
                )
                product_dashboard.save()
                return_product_array.append(product_dashboard.id)
            else:
                cat_prod = CategoryProductDashboard.objects.filter(name=prod.product.category_product).first()
                product_dashboard = Product(
                    id_category_product=cat_prod,
                    name_product=prod.product.name_product,
                    amount=prod.amount,
                    price_product=prod.price_product
                )
                product_dashboard.save()
                return_product_array.append(product_dashboard.id)
        return return_product_array

    @staticmethod
    def create_client(element):
        print('create_client')
        client = Client(name=element['name_customer'],
                        surname=element['customer_last_name'],
                        zip_code=element['zip_code'])
        client.save()
        return client

    @staticmethod
    def create_sales(id_client, id_data, id_product, total_price):
        print('create_sales')
        sales = Sales(id_client=id_client, id_data=id_data, total_price=total_price)
        sales.save()
        sales.id_product.set(id_product)

