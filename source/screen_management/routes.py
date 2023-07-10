from fastapi import APIRouter, File
from starlette import status
from starlette.responses import Response

from source.screen_management.services import ScreenTrackingServices

router = APIRouter(prefix='/screenshot-management', tags=['Screenshot Management'])

screenshot_services = ScreenTrackingServices()


@router.get('/make_screenshots/')
async def make_screenshots():
    url_path_names = await screenshot_services.return_url_path_names()
    await screenshot_services.screenshot_utils.make_screenshot(url_path_names=url_path_names)


