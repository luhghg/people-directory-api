from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date



class PersonsResponse(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=128)
    work_email: EmailStr
    phone: int 
    photo_url: str = Field(max_length=200)

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(BaseModel):

    first_name: str
    last_name: str
    work_email: EmailStr
    phone: int
    photo_url: str

    date_of_birth: date
    home_adress: str
    national_id: int
