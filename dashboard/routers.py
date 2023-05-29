from dashboard.models import Data, CategoryProduct, Product, Client, Sales


class MyRouter(object):

    @staticmethod
    def db_for_read(model, **hints):
        if model == Data or model == CategoryProduct or model == Product or model == Client or model == Sales:
            return 'data_warehouse'
        return None

    @staticmethod
    def db_for_write(model, **hints):
        if model == Data or model == CategoryProduct or model == Product or model == Client or model == Sales:
            return 'data_warehouse'
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        if app_label == 'data_warehouse':
            return db == 'data_warehouse'
        return None
