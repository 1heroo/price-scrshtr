import time

import asyncio
from PIL import Image
from source.core.settings import settings
from source.core.utils import BaseUtils
from selenium import webdriver


class SeleniumUtils(BaseUtils):

    def init_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        # options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        options.add_argument("Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        options.add_argument("accept=*/*")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Remote(command_executor=settings.SELENIUM_HOST + '/wd/hub', options=options)

        return driver

    async def compress_images(self, url_path_names):
        for url, path_name in url_path_names:
            img = Image.open(path_name)
            img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            img.save(path_name, optimize=True)

    async def make_screenshot(self, url_path_names: str):
        driver = self.init_driver()

        wb_url = 'https://www.wildberries.ru/catalog/153211620/detail.aspx'
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
        tabs_paths = []
        for index, pair in enumerate(url_path_names, start=1):
            tab_name = f'tab{index}'
            url, path_name = pair
            driver.execute_script(f"window.open('about:blank', '{tab_name}');")
            driver.switch_to.window(tab_name)
            driver.get(url)
            tabs_paths.append((tab_name, path_name))

        for tab, path_name in tabs_paths:
            driver.switch_to.window(tab)
            driver.save_screenshot(path_name)

        driver.quit()
        # driver.close()
