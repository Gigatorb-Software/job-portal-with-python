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
    middle_name: Optional[str] = None
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

class OrganizationProfileUpdate(BaseModel):
    company_description: Optional[str] = None  # Optional field
    # industry: Optional[str] = None  # Optional field
    city: Optional[str] = None  # Optional field
    state: Optional[str] = None  # Optional field
    country: Optional[str] = None  # Optional field
    website: Optional[HttpUrl] = None  # Optional field with URL validation


class OrganizationProfileResponse(BaseModel):
    user_email: str
    company_name: Optional[str]
    company_description: Optional[str]
    industry: Optional[str]
    website: Optional[HttpUrl] = None

class FileCreate(BaseModel):
    filename: str
    content_type: str
    class Config:
        from_attributes = True

# # Enum for experience level
# class ExperienceLevelEnum(str, Enum):
#     zero_to_one = "0-1 year"
#     one_to_two = "1-2 years"
#     two_to_five = "2-5 years"
#     five_plus = "5+ years"

# # Enum for education level
# class EducationLevelEnum(str, Enum):
#     high_school = "High School"
#     bachelors = "Bachelor's"
#     masters = "Master's"
#     phd = "Ph.D."

# Pydantic schema for JobPostModel
class JobPostCreateSchema(BaseModel):
    job_title: str = Field(..., max_length=100)
    description: str
    skills: Optional[str]
    salary: Optional[str]
    experience: str
    positions: int
    location: str
    education: str
    email: EmailStr
    role: str
    profile_completion: bool

class JobPostUpdateSchema(BaseModel):
    job_title: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    skills: Optional[str] 
    salary: Optional[str]
    experience: Optional[str]
    positions: Optional[int]
    location: Optional[str]
    education: Optional[str]
    active: Optional[bool] = True

class JobPostResponseSchema(BaseModel):
    job_id: int
    posted_by: str
    job_title: str
    description: str
    skills: Optional[str]
    salary: Optional[str]
    experience: Optional[str]
    positions: int
    location: Optional[str]
    education: Optional[str]
    created_at: datetime
    updated_at: datetime
    active: bool

    class Config:
        from_attributes = True

class ApplicationStatus(str, Enum):
    pending='pending'
    accepted='accepted'
    rejected='rejected'

class ApplicationCreateSchema(BaseModel):
    job_id: int
    job_seeker_email: EmailStr
    status: ApplicationStatus = ApplicationStatus.pending
    class Config:
        from_attributes = True


class StatusUpdateRequest(BaseModel):
    status: str
