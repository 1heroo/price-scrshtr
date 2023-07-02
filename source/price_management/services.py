import asyncio
import datetime
import time

import pandas as pd
import random
import string

from starlette.background import BackgroundTasks

from source.price_management.selenium_utils import SeleniumUtils
from source.price_management.utils import PriceManagementUtils
from source.supplier_management.models import Product, Report
from source.supplier_management.queries import SupplierQueries, ProductQueries, ReportQueries
from source.supplier_management.utils import ParsingUtils


class PriceManagementServices:

    def __init__(self):
        self.pm_utils = PriceManagementUtils()
        self.parsing_utils = ParsingUtils()

        self.selenium_utils = SeleniumUtils()
        self.supplier_queries = SupplierQueries()
        self.product_queries = ProductQueries()
        self.report_queries = ReportQueries()

        self.date_time_format_str = '%m/%d/%Y %H:%M:%S'

    async def price_management(self):
        awaiting_articles = self.pm_utils.get_awaiting_articles()
        blocked_articles = self.pm_utils.get_blocked_articles()
        blocked_articles = self.pm_utils.unblock_time_expired_articles(
            blocked_articles=blocked_articles, cached_time_format=self.date_time_format_str)
        print(awaiting_articles)
        print(blocked_articles)

        saved_products = await self.product_queries.fetch_all()

        nm_ids = [product.nm_id for product in saved_products]
        nm_ids = self.pm_utils.exclude_awaiting_articles(awaiting_articles=awaiting_articles, all_nm_ids=nm_ids)
        nm_ids = self.pm_utils.exclude_blocked_articles(blocked_articles=blocked_articles, all_nm_ids=nm_ids)

        products = await self.parsing_utils.get_detail_by_nm_ids(nm_ids=nm_ids)
        products = [product for product in products if 'qty' in str(product.get('sizes'))]

        saved_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'saved_product': product}
            for product in saved_products
        ])
        products_df = pd.DataFrame([
            {'nm_id': product.get('id'), 'product': product}
            for product in products
        ])
        if products_df.empty:

            return []

        df = pd.merge(saved_products_df, products_df, how='inner', left_on='nm_id', right_on='nm_id')

        products_to_be_saved = []
        new_awaiting_articles = []
        new_blocked_articles = []

        for index in df.index:
            saved_product: Product = df['saved_product'][index]
            product: dict = df['product'][index]

            product_priceU = product.get('priceU', 0) // 100
            product_salePriceU = product.get('salePriceU', 0) // 100

            product_clientSale = product.get('extended', {}).get('clientSale')
            product_basicSale = product.get('extended', {}).get('basicSale')

            if product_salePriceU < saved_product.rrc:
                awaiting_block_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
                awaiting_block_time_str = awaiting_block_time.strftime(self.date_time_format_str)

                new_awaiting_articles.append((
                    saved_product.nm_id, awaiting_block_time_str))

                block_time = datetime.datetime.now() + datetime.timedelta(hours=3)
                block_time_str = block_time.strftime(self.date_time_format_str)

                new_blocked_articles.append((
                    saved_product.nm_id, block_time_str
                ))

            saved_product.priceU = product_priceU
            saved_product.salePriceU = product_salePriceU
            saved_product.clientSale = product_clientSale
            saved_product.basicSale = product_basicSale
            products_to_be_saved.append(saved_product)

        await self.product_queries.save_in_db(instances=products_to_be_saved, many=True)
        self.pm_utils.set_awaiting_articles(awaiting_articles=new_awaiting_articles, settled_awaiting_articles=awaiting_articles)
        self.pm_utils.set_blocked_articles(settled_blocked_articles=blocked_articles, blocked_articles=new_blocked_articles)

    async def track_awaiting_articles(self):
        sellers = await self.supplier_queries.fetch_all()
        seller_dict = dict()

        for seller in sellers:
            seller_dict[seller.seller_id] = seller

        awaiting_articles = self.pm_utils.get_awaiting_articles()

        df = pd.DataFrame(awaiting_articles, columns=['nm_id', 'block_time'])

        df['block_time'] = df['block_time'].apply(lambda item: datetime.datetime.strptime(item, self.date_time_format_str))

        awaiting_df = df[df['block_time'] > datetime.datetime.now()]
        awaiting_df['block_time'] = awaiting_df['block_time'].apply(lambda item: item.strftime(self.date_time_format_str))
        awaiting_articles = awaiting_df.values.tolist()
        self.pm_utils.set_awaiting_articles(settled_awaiting_articles=[], awaiting_articles=awaiting_articles)

        screenshot_df = df[df['block_time'] <= datetime.datetime.now()]
        if screenshot_df.empty: return []

        nm_ids = list(screenshot_df['nm_id'])

        saved_products = await self.product_queries.get_products_by_nm_ids(nm_ids=nm_ids)
        saved_products_df = pd.DataFrame([
            {'nm_id': product.nm_id, 'saved_product': product}
            for product in saved_products
        ])

        products = await self.parsing_utils.get_detail_by_nm_ids(nm_ids=nm_ids)
        products = [product for product in products if 'qty' in str(product.get('sizes'))]

        products_df = pd.DataFrame([
            {'nm_id': product.get('id'), 'product': product}
            for product in products
        ])

        if products_df.empty: return

        df = pd.merge(saved_products_df, products_df, how='inner', left_on='nm_id', right_on='nm_id')

        products_to_be_saved = []
        reports_to_be_saved = []

        for index in df.index:
            saved_product: Product = df['saved_product'][index]
            product: dict = df['product'][index]

            product_priceU = product.get('priceU', 0) // 100
            product_salePriceU = product.get('salePriceU', 0) // 100

            product_clientSale = product.get('extended', {}).get('clientSale')
            product_basicSale = product.get('extended', {}).get('basicSale')

            if product_salePriceU < saved_product.rrc:
                report = self.pm_utils.prepare_report_for_saving(
                    seller_dict=seller_dict, saved_product=saved_product, product_dict=product)
                reports_to_be_saved.append(report)

            saved_product.priceU = product_priceU
            saved_product.salePriceU = product_salePriceU
            saved_product.clientSale = product_clientSale
            saved_product.basicSale = product_basicSale
            products_to_be_saved.append(saved_product)

        await self.product_queries.save_in_db(products_to_be_saved, many=True)
        await self.report_queries.save_in_db(instances=reports_to_be_saved, many=True)
        return reports_to_be_saved

    async def make_screenshots(self, reports: list[Report], background_tasks: BackgroundTasks):

        url_path_names = [(report.product_link, report.screen_link) for report in reports]
        background_tasks.add_task(self.selenium_utils.make_screenshot, url_path_names=url_path_names)
