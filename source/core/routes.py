from fastapi import APIRouter
from source.supplier_management.routes import router as supplier_router
from source.screen_management.routes import router as screen_router


router = APIRouter(prefix='/api/v1')

router.include_router(router=supplier_router)
router.include_router(router=screen_router)