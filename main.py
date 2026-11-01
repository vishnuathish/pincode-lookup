from fastapi   import FastAPI
from exceptions import PincodeNotFoundError, InvalidPincodeError, pincode_not_found_handler, invalid_pincode_handler
from models import PincodeRequest, LocationResponse, BulkRequest, BulkResponse
from data import pincode_db

app = FastAPI(title="Pincode lookup API", description="Auto fill city, state and district based on pincode")


#  Register your custom exception handlers
app.add_exception_handler(PincodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError, invalid_pincode_handler)



@app.get('/')
def root():
    return {"message": "Welcome to the Pincode lookup API. Use the endpoint /pincode/to get city, state, and district information."}


@app.get('/pincode/{code}', response_model=LocationResponse)
def lookup_pincode(code: str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincodeError(code, reason="Pincode must be a 6-digit number.")

    if code not in pincode_db:
        raise PincodeNotFoundError(code)
    return pincode_db[code]


@app.post('/bulkpincode', response_model=BulkResponse)
def bulk_lookup_pincodes(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )