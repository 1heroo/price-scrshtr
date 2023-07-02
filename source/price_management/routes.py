from fastapi import APIRouter
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import Response

from source.price_management.services import PriceManagementServices
from source.supplier_management.models import Report

router = APIRouter(prefix='/price-management', tags=['Price Management'])


price_services = PriceManagementServices()


@router.get('/launch-price-management/')
async def launch_price_management(background_tasks: BackgroundTasks):
    # tracking_blocked_articles
    await price_services.price_management()

    # screenshoting blocked_articles
    reports = await price_services.track_awaiting_articles()

    if reports:
        await price_services.make_screenshots(reports=reports, background_tasks=background_tasks)
    return Response(status_code=status.HTTP_200_OK)

