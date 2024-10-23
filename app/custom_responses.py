from fastapi.responses import JSONResponse

def ResponseSuccess(status_code: int, data: any):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data
        }
    )

def ResponseFailed(status_code: int, message: any):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": str(message)
        }
    )

