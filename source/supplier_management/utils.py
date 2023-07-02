import asyncio
from itertools import chain

import aiohttp

from source.core.utils import BaseUtils
from source.supplier_management.models import Product


class SupplierUtils(BaseUtils):

    @staticmethod
    def prepare_products_for_saving(
            products: list[dict], nm_id_column: str, rrc_column: str, supplier_id: int, vendor_code_column: str):
        return [
            Product(
                nm_id=product.get(nm_id_column),
                rrc=product.get(rrc_column),
                vendor_code=product.get(vendor_code_column),
                supplier_id=supplier_id
            )
            for product in products
        ]


class ParsingUtils(BaseUtils):

    async def get_details(self, nm_ids: list[int], session: aiohttp.ClientSession):
        url = 'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-2162195' \
              '&regions=80,38,4,64,83,33,68,70,69,30,86,75,40,1,66,110,22,31,48,71,114&spp=31' \
              f'&nm={";".join(nm_ids)}'
        data = await self.make_fast_get_request(url=url, session=session)
        if data:
            return data.get('data', {}).get('products', [])
        return []

    async def get_detail_by_nm_ids(self, nm_ids: list[int]):
        nm_ids = list(map(str, nm_ids))
        output_data = []

        async with aiohttp.ClientSession() as session:
            for index in range(0, len(nm_ids), 10_000):
                chink_nm_ids = nm_ids[index: index + 10_000]
                tasks = [
                    asyncio.create_task(
                        self.get_details(
                            nm_ids=chink_nm_ids[chunk_index: chunk_index + 100],
                            session=session
                        )
                    )
                    for chunk_index in range(0, len(chink_nm_ids), 100)
                ]
                output_data += list(chain(*(await asyncio.gather(*tasks))))
        return output_data

