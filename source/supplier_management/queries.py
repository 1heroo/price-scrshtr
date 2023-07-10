import pandas as pd
import sqlalchemy as sa
from source.db.db import async_session

from source.db.queries import BaseQueries
from source.supplier_management.models import Product, Screenshot


class ProductQueries(BaseQueries):
    model = Product

    async def fetch_all(self) -> list[Product]:
        async with async_session() as session:
            result = await session.execute(
                sa.select(self.model)
            )
            return result.scalars().all()

    async def save_or_pass(self, products: list[Product]):
        saved_products = await self.fetch_all()
        if not saved_products:
            await self.save_in_db(instances=products, many=True)
            return

        saved_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'saved_product': product}
            for product in saved_products
        ])
        products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'new_product': product}
            for product in products
        ])
        df = pd.merge(saved_products_df, products_df, how='outer', left_on='nm_id', right_on='nm_id')

        products_to_be_saved = []
        for index in df.index:
            saved_product: Product = df['saved_product'][index]
            new_product: Product = df['new_product'][index]

            if pd.isna(saved_product) and not pd.isna(new_product):
                products_to_be_saved.append(new_product)
        await self.save_in_db(instances=products_to_be_saved, many=True)




class ScreenshotQueries(BaseQueries):
    model = Screenshot

    async def fetch_all(self) -> list[Screenshot]:
        async with async_session() as session:
            result = await session.execute(
                sa.select(self.model)
            )
            return result.scalars().all()

