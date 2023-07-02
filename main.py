from fastapi import FastAPI
from sqladmin import Admin
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from source.core.routes import router as main_router
import uvicorn

from source.db.db import async_engine
from source.redis_cache.redis_client import redis_client
# from source.price_management.selenium_utils import SeleniumUtils
from source.supplier_management.admin import ProductAdmin, SupplierAdmin, ReportAdmin

app = FastAPI(title='Контроль РРЦ(Ресанта, Вихрь, Hunter)')

app.include_router(router=main_router)


app.mount("/static", StaticFiles(directory="static"), name="static")


admin = Admin(app=app, engine=async_engine)

admin.add_view(SupplierAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ReportAdmin)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
