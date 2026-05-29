import re

from pydantic import BaseModel, EmailStr, Field, field_validator

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    first_name: str = Field(..., min_length=3, max_length=32)
    last_name: str = Field(..., min_length=3, max_length=32)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    def password_complexity(cls, v: str) ->str:
        msg = []

        if not re.search(r'\d', v):
            msg.append('Password must contain at least one number')

        if not re.search(r'[a-z]', v):
            msg.append('Password must contain at least one lowercase letter')

        if not re.search(r'[A-Z]', v):
            msg.append('Password must contain at least one uppercase letter')

        if not re.search(r'[!@#$%^&*()?]', v):
            msg.append('Password must contain at least one special character (!@#$%^&*?)')

        if msg:
            raise ValueError(f"{'; '.join(msg)}.")

        return v