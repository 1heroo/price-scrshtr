from source.core.settings import settings
from source.core.utils import BaseUtils
from selenium import webdriver


class SeleniumUtils(BaseUtils):

    def __init__(self):
        self.driver = webdriver.Remote(command_executor=settings.SELENIUM_HOST + '/wd/hub')

    async def make_screenshot(self, url, path_name: str):
        self.driver.get(url=url)
        self.driver.save_screenshot(path_name)
