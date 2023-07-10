import asyncio
import datetime
import time

import pandas as pd
import random
import string

from starlette.background import BackgroundTasks

from source.screen_management.selenium_utils import SeleniumUtils
from source.supplier_management.models import Screenshot
from source.supplier_management.queries import ProductQueries, ScreenshotQueries
from source.supplier_management.utils import ParsingUtils


class ScreenTrackingServices:

    def __init__(self):
        self.screenshot_utils = SeleniumUtils()

        self.product_queries = ProductQueries()
        self.screenshot_queries = ScreenshotQueries()

    async def return_url_path_names(self):
        products = await self.product_queries.fetch_all()

        screenshots = []
        url_path_names = []
        for product in products:
            now = datetime.datetime.now()
            screenshot_path = f'static/screenshots/{product.nm_id}_{now.strftime("%m_%d_%Y_%H.%M.%S")}.png'

            screenshots.append(Screenshot(
                nm_id=product.nm_id,
                screenshot_path=screenshot_path,
                created_at=now
            ))
            url_path_names.append((
                f'https://www.wildberries.ru/catalog/{product.nm_id}/detail.aspx',
                screenshot_path
            ))
            await self.screenshot_queries.save_in_db(instances=screenshots, many=True)

        return url_path_names
