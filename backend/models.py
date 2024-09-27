from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, DateTime, Enum, LargeBinary, CheckConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGBLOB 

Base = declarative_base()

# UserModel
class UserModel(Base):
    __tablename__ = "users"

    first_name = Column(String(100), index=True)
    middle_name = Column(String(100), index=True, nullable=True)
    last_name = Column(String(100), index=True)
    email = Column(String(100), primary_key=True, index=True, unique=True)
    password = Column(String(100))
    registered_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    profile_completion = Column(Boolean, default=False)
    
    # Role field with limited choices
    role = Column(String(50), nullable=False, default="job_seeker")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role not in ["job_seeker", "organization"]:
            raise ValueError("Role must be either 'job_seeker' or 'organization'")

# JobSeekerProfileModel
class JobSeekerProfileModel(Base):
    __tablename__ = "job_seeker_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    user_email = Column(String(100), ForeignKey("users.email"), index=True)
    dob = Column(Date, nullable=True)  # Optional field
    bio = Column(Text, nullable=True)  # Optional field
    address = Column(Text, nullable=True)  # Optional field
    skills = Column(Text, nullable=True)  # Optional field
    experience = Column(String(100), nullable=True)  # Optional field
    education = Column(String(100), nullable=True)  # Optional field
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", backref="job_seeker_profile", cascade="all, delete")

# OrganizationProfileModel
class OrganizationProfileModel(Base):
    __tablename__ = "organization_profiles"
    
    user_email = Column(String(100), ForeignKey("users.email"), index=True)
    company_name = Column(String(100), primary_key=True, index=True)
    company_description = Column(Text, nullable=True)  # Optional field
    industry = Column(String(100), nullable=True)  # Optional field
    city = Column(String(100), nullable=True)  # Optional field
    state = Column(String(100), nullable=True)  # Optional field
    country = Column(String(100), nullable=True)  # Optional field
    website = Column(String(100), nullable=True)  # Optional field
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", backref="organization_profile", cascade="all, delete")

# JobPostModel
class JobPostModel(Base):
    __tablename__ = "job_posts"

    job_id = Column(Integer, primary_key=True, index=True)
    posted_by = Column(String(100), ForeignKey("organization_profiles.user_email"), index=True)
    job_title = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    skills = Column(Text, nullable=True)  # Optional field
    salary = Column(String(100), nullable=True)  # Optional field
    
    # Experience level enum
    experience = Column(Enum('0-1 year', '1-2 years', '2-5 years', '5+ years', name='experience_level'), nullable=False)
    positions = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)
    
    # Education level enum
    education = Column(Enum('High School', 'Bachelor\'s', 'Master\'s', 'Ph.D.', name='education_level'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)

    organization = relationship("OrganizationProfileModel", backref="job_posts", cascade="all, delete")

# FileModel
class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(100), ForeignKey("users.email"), index=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    
    # Specify file type: resume, profile_picture, or company_logo
    file_type = Column(String(50), nullable=False)
    file_content = Column(LONGBLOB, nullable=False)

    # Corrected CheckConstraint syntax for file_type values
    __table_args__ = (
        CheckConstraint("file_type IN ('resume', 'profile_picture', 'company_logo')", name='check_file_type'),
    )
    user = relationship("UserModel", backref="files", cascade="all, delete")


# from sqlalchemy import Enum as SAEnum
# from enum import Enum as PyEnum

# class ApplicationStatus(PyEnum):
#     PENDING = 'pending'
#     ACCEPTED = 'accepted'
#     REJECTED = 'rejected'

# class ApplicantModel(Base):
#     __tablename__ = "applicants"
    
#     applicant_id = Column(Integer, primary_key=True, index=True)
#     applied_by_email = Column(String(100), ForeignKey("users.email"))
#     posted_by_email = Column(String(100), ForeignKey("organization_profiles.user_email"))
#     job_id = Column(Integer, ForeignKey("job_posts.id"))
    
#     status = Column(SAEnum(ApplicationStatus), nullable=False)
    
#     user = relationship("UserModel", backref="applicants")
#     organization = relationship("OrganizationProfileModel", backref="applicants")
#     job = relationship("JobPostModel", backref="applicants")
    
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     __table_args__ = (
#         ForeignKeyConstraint(
#             ["posted_by_email"],
#             ["organization_profiles.user_email"],
#             ondelete="CASCADE",
#             onupdate="CASCADE"
#         ),
#         ForeignKeyConstraint(
#             ["job_id"],
#             ["job_posts.id"],
#             ondelete="CASCADE",
#             onupdate="CASCADE"
#         ),
#     )
    
#     class Config:
#         arbitrary_types_allowed = True
