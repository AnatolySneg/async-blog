import re

from pydantic import BaseModel, EmailStr, Field, field_validator

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    first_name: str = Field(..., min_length=3, max_length=32)
    last_name: str = Field(..., min_length=3, max_length=32)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    def password_complexity(cls, value: str) ->str:
        msg = []

        if not re.search(r'\d', value):
            msg.append('Password must contain at least one number')

        if not re.search(r'[a-z]', value):
            msg.append('Password must contain at least one lowercase letter')

        if not re.search(r'[A-Z]', value):
            msg.append('Password must contain at least one uppercase letter')

        if not re.search(r'[!@#$%^&*()?]', value):
            msg.append('Password must contain at least one special character (!@#$%^&*?)')

        if msg:
            raise ValueError(f"{'; '.join(msg)}.")

        return value
    
    
class UserResponse(BaseModel):                                                                                                                                                                                    
    id: int
    username: str
    email: EmailStr

class RegistrationResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"