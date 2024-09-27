from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional
from fastapi import UploadFile
from models import *
from pydantic import BaseModel, Field, HttpUrl, constr

from enum import Enum  # Make sure you're importing the correct Enum

# # Define the RoleName enum
class RoleName(str, Enum):
    job_seeker = 'job_seeker'
    organization = 'organization'


class UserCreate(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr
    password: str
    role: RoleName

    class Config:
        from_attributes = True
        populate_by_name = True

class UserResponse(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: Optional[str]
    last_name: str
    registered_at: datetime
    updated_at: datetime
    role: RoleName

    class Config:
        from_attributes = True
        populate_by_name = True


class Login(BaseModel):
    email: EmailStr
    password: str


class JobSeekerProfileCreate(BaseModel):
    title: str
    user_email: EmailStr
    dob: Optional[date]
    bio: Optional[str] # Optional field
    address: Optional[str]  # Optional field
    skills: Optional[str]  # Optional field
    experience: Optional[str]  # Optional field
    education: Optional[str]  # Optional field

class JobSeekerProfileResponse(BaseModel):
    id: int
    user_email: str
    bio: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    address: Optional[str]
    dob: Optional[date]

class OrganizationProfileCreate(BaseModel):
    user_email: EmailStr  # Email must be a valid email format
    company_name: constr(max_length=100)  # Limit length to 100 characters
    company_description: Optional[str] = None  # Optional field
    industry: Optional[str] = None  # Optional field
    city: Optional[str] = None  # Optional field
    state: Optional[str] = None  # Optional field
    country: Optional[str] = None  # Optional field
    website: Optional[HttpUrl] = None  # Optional field with URL validation



class OrganizationProfileResponse(BaseModel):
    id: int
    user_email: str
    company_name: Optional[str]
    company_description: Optional[str]
    industry: Optional[str]
    website: Optional[str]


class FileCreate(BaseModel):
    filename: str
    content_type: str

    class Config:
        from_attributes = True