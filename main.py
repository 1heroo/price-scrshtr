from fastapi import FastAPI
from sqladmin import Admin
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from source.core.routes import router as main_router
import uvicorn

from source.db.db import async_engine
from source.price_management.selenium_utils import SeleniumUtils
from source.supplier_management.admin import ProductAdmin, SupplierAdmin


app = FastAPI(title='Контроль РРЦ(Ресанта, Вихрь, Hunter)')

app.include_router(router=main_router)


@app.get('/test')
async def test():
    utils = SeleniumUtils()
    url = 'https://www.wildberries.ru/catalog/154257090/detail.aspx?targetUrl=SG'
    url = 'http://web:8000/test/test'
    await utils.make_screenshot(url=url, path_name='static/screenshots/ss.png')


@app.get('/test/test')
async def test_test(request: Request):
    print(request.headers)

    print('\n\n\n\n')

    print(request.cookies)


app.mount("/static", StaticFiles(directory="static"), name="static")


admin = Admin(app=app, engine=async_engine)

admin.add_view(SupplierAdmin)
admin.add_view(ProductAdmin)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
