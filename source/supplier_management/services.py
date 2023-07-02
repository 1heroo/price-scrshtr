import pandas as pd

from source.core.xlsx_utils import XlsxUtils
from source.supplier_management.models import Supplier
from source.supplier_management.queries import ProductQueries, SupplierQueries, ReportQueries
from source.supplier_management.utils import ParsingUtils, SupplierUtils


class SupplierServices:

    def __init__(self):
        self.supplier_utils = SupplierUtils()
        self.parsing_utils = ParsingUtils()

        self.xlsx_utils = XlsxUtils()

        self.supplier_queries = SupplierQueries()
        self.product_queries = ProductQueries()
        self.report_queries = ReportQueries()


    async def import_products(
            self, df: pd.DataFrame, nm_id_column: str, rrc_column: str, seller_id_column: str, vendor_code_column: str):
        products = df.to_dict('records')

        suppliers = await self.supplier_queries.fetch_all()
        suppliers_dict = dict()
        for seller in suppliers:
            suppliers_dict[seller.seller_id] = seller

        sellers_products = dict()
        for product in products:
            seller_id = product.get(seller_id_column)
            if sellers_products.get(seller_id):
                sellers_products[seller_id].append(product)
            else:
                sellers_products[seller_id] = [product]

        for seller_id, products in sellers_products.items():
            seller: Supplier = suppliers_dict.get(seller_id)
            if seller is None: continue

            products_to_be_saved = self.supplier_utils.prepare_products_for_saving(
                products=products, nm_id_column=nm_id_column, rrc_column=rrc_column,
                supplier_id=seller.id, vendor_code_column=vendor_code_column)
            await self.product_queries.save_or_update_for_supplier(products=products_to_be_saved, supplier_id=seller.id)

    async def get_price_violations(self):
        reports = await self.report_queries.fetch_all()
        return [
            report.to_dict()
            for report in reports
        ]


