from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date



class PersonsResponse(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=128)
    work_email: EmailStr
    phone: int
    photo_url: str = Field(max_length=200)

    model_config = ConfigDict(from_attributes=True)


class PersonsResponseAdmin(BaseModel):
    id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=128)
    work_email: EmailStr
    phone: int
    photo_url: str = Field(max_length=200)

    date_of_birth: date
    home_adress: str
    national_id: int

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


class PersonUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    work_email: EmailStr | None = None
    phone: int | None = None
    photo_url: str | None = None

    date_of_birth: date | None = None
    home_adress: str | None = None
    national_id: int | None = None
