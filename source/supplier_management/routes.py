import pandas as pd
from fastapi import APIRouter, File
from starlette import status
from starlette.responses import Response

from source.supplier_management.models import Product
from source.supplier_management.services import SupplierServices

router = APIRouter(prefix='/supplier-management', tags=['Supplier Management'])


supplier_services = SupplierServices()


@router.post('/import-products/')
async def import_products(file: bytes = File()):
    df = pd.read_excel(file)
    nm_id_column = df['Артикул WB'].name
    rrc_column = df['РРЦ'].name
    seller_id_column = df['ID SHOP'].name
    vendor_code_column = df['Артикул'].name
    df = df.dropna(subset=[nm_id_column, rrc_column, seller_id_column, vendor_code_column])
    df = df.drop_duplicates(subset=[nm_id_column, rrc_column, seller_id_column, vendor_code_column])

    await supplier_services.import_products(
        df=df, nm_id_column=nm_id_column, rrc_column=rrc_column,
        seller_id_column=seller_id_column, vendor_code_column=vendor_code_column)

    return Response(status_code=status.HTTP_200_OK)
