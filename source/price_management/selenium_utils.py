import time

from source.core.settings import settings
from source.core.utils import BaseUtils
from selenium import webdriver
"""    standard_cookie = 'WBToken={wb_token}; x-supplier-id-external={supplier_external}; x-supplier-id={supplier_external}'

    @staticmethod
    def get_headers(x_user_id, cookie):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "X-User-Id": x_user_id,
            "Cookie": cookie,
        }"""


class SeleniumUtils(BaseUtils):

    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Remote(command_executor=settings.SELENIUM_HOST + '/wd/hub', options=options)

    def make_screenshot_headers(self, request):
        cookies = '___wbu=7746be94-e32a-45e7-84c9-aa25810afac5.1678980874; _wbauid=10007082101678980874; WILDAUTHNEW_V3=467E68D1E3CADCB8B3496BC550EF841575D62000E10A151A1D339D380ACEF611A67900B733DFFC1AED899F4A1507A207D7A91D157ED5030BB40D9343642AD3540EC083CB2FAC5699460760C8F35519E3A45C9F06E21D26E521A5E6D7DF862A746A166BE3026DDA33DFE3A3DDF619EB882362177EC75D80B217185362763E64483688459B31C6C5E0E1C20560C96FADDC46617FED82DEF6341B86692EB69BE0AC085446FA30F7BA0B4045660E7521DFFE03DFDC55FB709090AE01D4992D5152E91B60F924361052542764DF18127DDDA2E4B051D3B9AA923313E06A3290D6E894B85F453522D4670386B4655D027E55C8A580B4FB4E9692AD4D24B25EBD9D92101365AE45A4B3350AB73352519274BF11037FB12ACEB9323151E5AD1DB1443011553C5D73B73D80E4293625984515AB04F1D90546; _ym_uid=1682177965141817807; _ym_d=1682177965; x-supplier-id-external=b4c30a97-e483-5a84-86b6-381fe172e298; um=uid%3Dw7TDssOkw7PCu8K4wrbCt8KywrLCt8Kxwrc%253d%3Aproc%3D100%3Aehash%3Dd41d8cd98f00b204e9800998ecf8427e; ___wbs=a5dcab5b-a900-46f8-989f-2874b58fa5a7.1688229443; __wba_s=1; __spp='
        bearer = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODc4NjU4OTEsInZlcnNpb24iOjIsInVzZXIiOiI5NzYzMzYwNiIsInNoYXJkX2tleSI6IjE1In0.cUqOkJRpxil529nWEa9Zsecznhv5o44TyAhzMOT_FVMRvakHoR_FOxvp6y5-rtG7oBwTvB7qh-XNKaM9TL2xkOg9w5XdzEx50Xj2aTVepExA-Q-j3KdlgPG6J-GvsgrOcDhs5lyVQHLhmBrKjV--94j2AI3kk2G2Wn8kbFft5sQBBLLD15kn-lZ9wfeIWWysOa6nzuM0HM7Q8Wa9Wwjt2yU3wj-DmO7XgmSkpqf2nHAsQvgJMm-7ClJ4abdMODonr3YdmZPiMnKRYZAUYjMq4HP-C5o93ABy24DIwJOTfAoa_xkLSWzmoYW9hki36wk-2k1o_bUR7o7ysMnwqbM-zA'
        request.headers['Cookie'] = cookies
        request.headers['Authorization'] = bearer
        request.headers['Referer'] = 'https://www.wildberries.ru/'

    async def make_screenshot(self, url, path_name: str):

        self.driver.request_interceptor = self.make_screenshot_headers
        self.driver.get(url=url)
        time.sleep(3)

        self.driver.save_screenshot(path_name)
