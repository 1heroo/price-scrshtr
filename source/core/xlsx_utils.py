import io
import os
import zipfile

import pandas as pd
from starlette.responses import Response, StreamingResponse
import typing


class XlsxUtils:

    @staticmethod
    def zip_response(filenames, zip_filename):
        s = io.BytesIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            fdir, fname = os.path.split(fpath)
            print(fpath)
            zf.write(fpath, fname)

        zf.close()

        for file in filenames:
            os.remove(file)

        resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
            'Content-Disposition': f'attachment;filename={zip_filename}'
        })
        return resp

    @staticmethod
    def streaming_response(sequence: typing.Sequence, file_name: str) -> StreamingResponse:
        df = pd.DataFrame(sequence)
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.close()

        return StreamingResponse(io.BytesIO(output.getvalue()),
                                 media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                 headers={'Content-Disposition': f'attachment; filename="{file_name}.xlsx"'})

