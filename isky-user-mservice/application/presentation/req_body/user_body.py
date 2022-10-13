from pydantic import BaseModel, Field


class UserEmailBody(BaseModel):
    email: str = Field(description="User email")
    
class UserNameBody(BaseModel):
    name: str = Field(description="User name")

class UserPasswordBody(BaseModel):
    password: str = Field(description="User password. Min length 5 characters", min_length=5)
    
class UserPhoneBody(BaseModel):
    phone: str = Field(description="Phone number")
    
class UserStatusBody(BaseModel):
    status: bool = Field(description="Is the user user active: True or False")

class UserEmailVerificationBody(BaseModel):
    verify: bool = Field(description="Email verification: True or False")
    
class UserPhoneVerificationBody(BaseModel):
    verify: bool = Field(description="Phone verification: True or False")