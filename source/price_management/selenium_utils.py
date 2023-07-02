import time

import asyncio

from source.core.settings import settings
from source.core.utils import BaseUtils
from selenium import webdriver


class SeleniumUtils(BaseUtils):

    def init_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.165 Safari/537.36")
        options.add_argument("accept=*/*")
        options.add_argument("--window-size=1920,1080")

        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Remote(command_executor=settings.SELENIUM_HOST + '/wd/hub', options=options)

        return driver

    async def make_screenshot(self, url_path_names: str):
        driver = self.init_driver()

        wb_url = 'https://www.wildberries.ru'
        driver.get(url=wb_url)
        driver.add_cookie({
            'name': '__spp',
            'value': '',
            'domain': 'wildberries.ru'
        })

        driver.add_cookie({
            'name': 'WILDAUTHNEW_V3',
            'value': settings.WILDAUTHNEW_V3,
            'domain': 'wildberries.ru'
        })
        for url, path_name in url_path_names:
            driver.get(url=url)
            await asyncio.sleep(4.2)
            driver.save_screenshot(path_name)

        driver.quit()
        driver.close()
