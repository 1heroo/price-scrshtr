from sqladmin import ModelView

from source.supplier_management.models import Supplier, Product


class SupplierAdmin(ModelView, model=Supplier):
    column_list = ['id', 'name', 'seller_id', 'is_active']
    column_searchable_list = ['name', 'seller_id']

    page_size = 100


class ProductAdmin(ModelView, model=Product):
    column_list = ['nm_id', 'salePriceU', 'priceU', 'clientSale', 'rrc', 'supplier']
    column_searchable_list = ['nm_id']

    page_size = 100


