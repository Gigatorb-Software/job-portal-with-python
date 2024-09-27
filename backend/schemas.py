from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from models import *
from pydantic import BaseModel, Field

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
    bio: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    user_email: EmailStr
    

class JobSeekerProfileResponse(BaseModel):
    id: int
    user_email: str
    bio: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    resume: Optional[str]  # file name or URL
    profile_picture: Optional[str]  #file name or URL

class OrganizationProfileCreate(BaseModel):
    company_name: Optional[str]
    company_description: Optional[str]
    industry: Optional[str]
    website: Optional[str]

class OrganizationProfileResponse(BaseModel):
    id: int
    user_email: str
    company_name: Optional[str]
    company_description: Optional[str]
    industry: Optional[str]
    logo: Optional[str]  # file name or URL
    website: Optional[str]


class FileCreate(BaseModel):
    filename: str
    content_type: str

    class Config:
        from_attributes = True