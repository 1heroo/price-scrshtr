from fastapi import APIRouter
from source.supplier_management.routes import router as supplier_router
from source.price_management.routes import router as price_router


router = APIRouter(prefix='/api/v1')

router.include_router(router=supplier_router)
router.include_router(router=price_router)