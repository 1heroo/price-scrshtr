import pandas as pd

from source.price_management.utils import PriceManagementUtils
from source.supplier_management.models import Product
from source.supplier_management.queries import SupplierQueries, ProductQueries
from source.supplier_management.utils import ParsingUtils


class PriceManagementServices:

    def __init__(self):
        self.pm_utils = PriceManagementUtils()
        self.parsing_utils = ParsingUtils()

        self.supplier_queries = SupplierQueries()
        self.product_queries = ProductQueries()

    async def price_management(self):
        saved_products = await self.product_queries.fetch_all()

        nm_ids = [str(product.nm_id) for product in saved_products]
        products = await self.parsing_utils.get_detail_by_nm_ids(nm_ids=nm_ids)

        saved_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'saved_product': product}
            for product in saved_products
        ])
        products_df = pd.DataFrame([
            {'nm_id': product.get('id'), 'product': product}
            for product in products
        ])

        df = pd.merge(saved_products_df, products_df, how='inner', left_on='nm_id', right_on='nm_id')

        products_to_be_saved = []
        for index in df.index:
            saved_product: Product = df['saved_product'][index]
            product: dict = df['product'][index]

            product_priceU = product.get('priceU', 0) // 100
            product_salePriceU = product.get('salePriceU', 0) // 100

            product_clientSale = product.get('extended', {}).get('clientSale')
            product_basicSale = product.get('extended', {}).get('basicSale')

            if product_salePriceU < saved_product.rrc:
                pass

            saved_product.priceU = product_priceU
            saved_product.salePriceU = product_salePriceU
            saved_product.clientSale = product_clientSale
            saved_product.basicSale = product_basicSale
            products_to_be_saved.append(saved_product)

        await self.product_queries.save_in_db(instances=products_to_be_saved, many=True)
