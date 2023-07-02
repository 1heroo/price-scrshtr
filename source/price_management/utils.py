import datetime
import json
import random
import string
import time

import pandas as pd

from source.core.utils import BaseUtils
from source.redis_cache.redis_client import redis_client
from source.supplier_management.models import Product, Report, Supplier


class PriceManagementUtils(BaseUtils):

    def prepare_report_for_saving(self, product_dict: dict, saved_product: Product, seller_dict: dict) -> Report:
        seller: Supplier = seller_dict.get(product_dict.get('supplierId'))

        return Report(
            product_title=product_dict.get('name'),
            pnc=saved_product.vendor_code,
            supplier_name=seller.name,
            product_link=f'https://www.wildberries.ru/catalog/{saved_product.nm_id}/detail.aspx',
            brand=product_dict.get('brand'),
            rrc=saved_product.rrc,
            company_price=product_dict.get('salePriceU', 0) // 100,
            date=datetime.date.today(),
            time=datetime.datetime.now().strftime('%H:%M'),
            screen_link=self.make_screenshot_link()
        )

    @staticmethod
    def unblock_time_expired_articles(blocked_articles, cached_time_format: str):
        df = pd.DataFrame(blocked_articles, columns=['nm_id', 'block_time'])

        df['block_time'] = df['block_time'].apply(
            lambda item: datetime.datetime.strptime(item, cached_time_format))

        blocked_articles_df = df[df['block_time'] >= datetime.datetime.now()]
        blocked_articles_df['block_time'] = blocked_articles_df['block_time'].apply(
            lambda item: item.strftime(cached_time_format))

        blocked_articles = blocked_articles_df.values.tolist()
        return blocked_articles

    @staticmethod
    def exclude_blocked_articles(all_nm_ids: str, blocked_articles):
        if not blocked_articles: return all_nm_ids

        nm_id_df = pd.DataFrame(all_nm_ids, columns=['nm_id'])

        awaiting_articles_df = pd.DataFrame(blocked_articles, columns=['blocked_nm_id', 'block_time'])
        df = pd.merge(nm_id_df, awaiting_articles_df, how='outer', left_on='nm_id', right_on='blocked_nm_id')

        prepared_nm_ids = [
            df['nm_id'][index]
            for index in df.index
            if pd.isna(df['blocked_nm_id'][index])
        ]
        return prepared_nm_ids

    @staticmethod
    def exclude_awaiting_articles(all_nm_ids: str, awaiting_articles):
        if not awaiting_articles: return all_nm_ids

        nm_id_df = pd.DataFrame(all_nm_ids, columns=['nm_id'])

        awaiting_articles_df = pd.DataFrame(awaiting_articles, columns=['awaiting_nm_id', 'block_time'])
        df = pd.merge(nm_id_df, awaiting_articles_df, how='outer', left_on='nm_id', right_on='awaiting_nm_id')

        prepared_nm_ids = [
            df['nm_id'][index]
            for index in df.index
            if pd.isna(df['awaiting_nm_id'][index])
        ]
        return prepared_nm_ids

    @staticmethod
    def set_awaiting_articles(settled_awaiting_articles, awaiting_articles):
        settled_awaiting_articles += awaiting_articles
        redis_client.mset({"awaiting_articles": json.dumps(settled_awaiting_articles)})

    @staticmethod
    def set_blocked_articles(settled_blocked_articles, blocked_articles):

        settled_blocked_articles += blocked_articles
        redis_client.mset({'blocked_articles': json.dumps(settled_blocked_articles)})

    @staticmethod
    def get_awaiting_articles():
        awaiting_articles = redis_client.get('awaiting_articles')
        if awaiting_articles is None:
            return []

        return json.loads(awaiting_articles)

    @staticmethod
    def get_blocked_articles():
        blocked_articles = redis_client.get('blocked_articles')
        if blocked_articles is None:
            return []
        return json.loads(blocked_articles)

    @staticmethod
    def make_screenshot_link():
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for _ in range(16))
        return f'static/screenshots/{rand_string}_{time.time()}.png'
