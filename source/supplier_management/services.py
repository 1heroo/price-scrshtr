import pandas as pd

from source.core.settings import settings
from source.core.xlsx_utils import XlsxUtils
from source.supplier_management.queries import ProductQueries, ScreenshotQueries, Product
from source.supplier_management.utils import ParsingUtils, SupplierUtils


class SupplierServices:

    def __init__(self):
        self.supplier_utils = SupplierUtils()
        self.parsing_utils = ParsingUtils()

        self.xlsx_utils = XlsxUtils()

        self.product_queries = ProductQueries()

    async def import_products(self, df: pd.DataFrame, nm_id_column: str):
        nm_ids = list(df[nm_id_column])
        products_to_be_saved = [
            Product(nm_id=nm_id)
            for nm_id in nm_ids
        ]
        await self.product_queries.save_or_pass(products=products_to_be_saved)





