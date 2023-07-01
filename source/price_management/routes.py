from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from source.price_management.services import PriceManagementServices

router = APIRouter(prefix='/price-management', tags=['Price Management'])


price_services = PriceManagementServices()


@router.get('/launch-price-management/')
async def launch_price_management():

    await price_services.price_management()
    return Response(status_code=status.HTTP_200_OK)

