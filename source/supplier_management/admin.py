from sqladmin import ModelView

from source.supplier_management.models import Product, Screenshot


class ProductAdmin(ModelView, model=Product):
    column_list = ['nm_id']
    column_searchable_list = ['nm_id']

    page_size = 100


class ScreenshotAdmin(ModelView, model=Screenshot):
    column_list = ['nm_id', 'screenshot_path', 'created_at']
    column_searchable_list = ['nm_id']
    column_default_sort = [('created_at', False)]
    page_size = 100
