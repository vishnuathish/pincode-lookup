from fastapi.responses import JSONResponse
from fastapi.requests import Request

class PincodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPincodeError(Exception):
    def __init__(self, pincode: str, reason: str = 'Invalid pincode'):
        self.pincode = pincode
        self.reason = reason

# Custom handler
async def pincode_not_found_handler(request: Request, exc: PincodeNotFoundError): 
    return JSONResponse(
        status_code=404,
        content={"message": f"Pincode {exc.pincode} not found."},
        pincode=exc.pincode
    )

async def invalid_pincode_handler(request: Request, exc: InvalidPincodeError): 
    return JSONResponse(
        status_code=400,
        content={"message": f"Pincode {exc.pincode} is invalid.", "reason": exc.reason},
        pincode=exc.pincode
    )