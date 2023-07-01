import time

from source.core.settings import settings
from source.core.utils import BaseUtils
from selenium import webdriver


class SeleniumUtils(BaseUtils):

    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(command_executor=settings.SELENIUM_HOST + '/wd/hub', options=options)

    async def make_screenshot(self, url, path_name: str):
        self.driver.get(url=url)
        time.sleep(3)

        self.driver.save_screenshot(path_name)
        print(path_name)