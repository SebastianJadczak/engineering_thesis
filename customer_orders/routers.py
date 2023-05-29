from customer_orders.models import CustomerOrder, ElementInCustomerOrder


class MyRouter(object):

    @staticmethod
    def db_for_read(model, **hints):
        if model == CustomerOrder or model == ElementInCustomerOrder:
            return 'default'
        return None

    @staticmethod
    def db_for_write(model, **hints):
        if model == CustomerOrder or model == ElementInCustomerOrder:
            return 'default'
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        if app_label == 'default':
            return db == 'default'
        return None
