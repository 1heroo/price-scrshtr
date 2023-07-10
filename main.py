from fastapi import FastAPI
from sqladmin import Admin
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from source.core.routes import router as main_router
import uvicorn

from source.db.db import async_engine
from source.screen_management.selenium_utils import SeleniumUtils
from source.supplier_management.admin import ProductAdmin, ScreenshotAdmin

app = FastAPI(title='Скрин трекинг цен')

app.include_router(router=main_router)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/test')
async def test():
    utils = SeleniumUtils()
    url = [('https://www.wildberries.ru/catalog/153211620/detail.aspx', 's.png')]
    await utils.make_screenshot(url_path_names=url)
    await utils.compress_images(url_path_names=url)


admin = Admin(app=app, engine=async_engine)


admin.add_view(ProductAdmin)
admin.add_view(ScreenshotAdmin)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
