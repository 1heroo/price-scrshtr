import pandas as pd
import sqlalchemy as sa
from source.db.db import async_session

from source.db.queries import BaseQueries
from source.supplier_management.models import Supplier, Product


class SupplierQueries(BaseQueries):
    model = Supplier

    async def fetch_all(self, only_active=False) -> list[Supplier]:
        async with async_session() as session:
            if only_active:
                result = await session.execute(
                    sa.select(self.model)
                    .where(self.model.is_active)
                )
            else:
                result = await session.execute(
                    sa.select(self.model)
                )
            return result.scalars().all()


class ProductQueries(BaseQueries):
    model = Product

    async def fetch_all(self) -> list[Product]:
        async with async_session() as session:
            result = await session.execute(
                sa.select(self.model)
            )
            return result.scalars().all()

    async def get_products_by_supplier_id(self, supplier_id: int) -> list[Product]:
        async with async_session() as session:
            result = await session.execute(
                sa.select(self.model)
                .where(self.model.supplier_id == supplier_id)
            )
            return result.scalars().all()

    async def save_or_update_for_supplier(self, products: list[Product], supplier_id: int):
        saved_products = await self.get_products_by_supplier_id(supplier_id=supplier_id)

        if not saved_products:
            await self.save_in_db(instances=products, many=True)
            return

        saved_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'saved_product': product}
            for product in saved_products
        ])
        new_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'new_product': product}
            for product in products
        ])
        df = pd.merge(saved_products_df, new_products_df, how='outer', left_on='nm_id', right_on='nm_id')

        products_to_be_saved = []
        for index in df.index:
            saved_product: Product = df['saved_product'][index]
            new_product: Product = df['new_product'][index]

            if pd.isna(saved_product):
                products_to_be_saved.append(new_product)
                continue

            saved_product.salePriceU = new_product.salePriceU
            saved_product.priceU = new_product.priceU
            saved_product.rrc = new_product.rrc
            saved_product.clientSale = new_product.clientSale
            saved_product.basicSale = new_product.basicSale
            products_to_be_saved.append(saved_product)
        await self.save_in_db(instances=products_to_be_saved, many=True)


