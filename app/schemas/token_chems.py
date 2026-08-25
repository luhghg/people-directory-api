from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

    
