from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode: str

    @field_validator('pincode')
    @classmethod
    def validate_pincode(cls, value):
        if not value.isdigit() or len(value) != 6:
            raise ValueError('Pincode must be a 6-digit number.')
        return value


class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str


class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator('pincodes')
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError('Pincodes list cannot be empty.')
        if( len(values) > 20): 
            raise ValueError('Pincodes list cannot contain more than 20 pincodes.')

        for code in values:
            if not code.isdigit() or len(code) != 6:
                raise ValueError(f'Pincode {code} must be a 6-digit number.')
        return values


class BulkResponse(BaseModel):
    status: str = 'success'
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str] = [] 