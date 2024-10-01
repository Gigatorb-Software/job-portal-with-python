from models import *
from schemas import *
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from typing import Dict

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        first_name=user.first_name,
        middle_name=user.middle_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role,
        password=pwd_context.hash(user.password),        
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if user and pwd_context.verify(password, user.password):
            return user  # Return the user object
        return HTTPException(status_code=500, detail=f"user not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to authenticate user: {str(e)}")

        
def create_job_seeker_profile(db: Session, js_profile: JobSeekerProfileCreate):
    # Check if user exists

    user = db.query(UserModel).filter(UserModel.email == js_profile.user_email).first()

    if user: 
        user.profile_completion = True

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if profile already exists for user
    if db.query(JobSeekerProfileModel).filter(JobSeekerProfileModel.user_email == js_profile.user_email).first():
        raise HTTPException(status_code=400, detail="Job seeker profile already exists for this user")

    db_js_profile = JobSeekerProfileModel(
        bio=js_profile.bio,
        skills=js_profile.skills,
        experience=js_profile.experience,
        education=js_profile.education,
        user_email=js_profile.user_email,
        dob=js_profile.dob,
        title=js_profile.title,
        address=js_profile.address
    )
    db.add(db_js_profile)
    db.commit()
    db.close()
    return db_js_profile


def create_organization_profile(db: Session, Or_profile: OrganizationProfileCreate):
    user = db.query(UserModel).filter(UserModel.email == Or_profile.user_email).first()
    if user: 
        user.profile_completion = True
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_or_profile = OrganizationProfileModel(
        user_email=Or_profile.user_email,
        company_name=Or_profile.company_name,
        company_description=Or_profile.company_description,
        industry=Or_profile.industry,
        city=Or_profile.city,
        state=Or_profile.state,
        country=Or_profile.country,
        website=Or_profile.website
    )
    db.add(db_or_profile)
    db.commit()
    db.refresh(db_or_profile)
    return db_or_profile


def apply_to_job(db: Session, application_data: ApplicationCreateSchema) -> Dict:
    try:
        # Retrieve job post details
        job_post = db.query(JobPostModel).filter(JobPostModel.job_id == application_data.job_id).first()
        if job_post is None:
            raise ValueError("Job post not found")
        # Retrieve applicant's resume
        resume = db.query(FileModel).filter(FileModel.user_email == application_data.job_seeker_email, 
                                            FileModel.file_type == 'resume').first()
        # Create job application
        applicant_data = JobApplicationModel(
            job_seeker_email=application_data.job_seeker_email,
            job_id=application_data.job_id,
            resume_id=resume.id if resume else None
        )
        print(applicant_data)
        # Add and commit application data

        db.add(applicant_data)
        db.commit()
        db.close()
        # Return application data with company name
        return {
            **applicant_data.__dict__,
            'company_name': job_post.company_name
        }
    except Exception as e:
        # Handle exceptions (e.g., log error, rollback database changes)
        print(f"Error applying to job: {str(e)}")
        return None


