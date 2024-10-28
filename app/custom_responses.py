from fastapi.responses import JSONResponse
from fastapi import status


def ResponseSuccess(status_code: int = status.HTTP_200_OK, data: any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data
        }
    )


def ResponseFailed(status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, message: any = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": str(message)
        }
    )
