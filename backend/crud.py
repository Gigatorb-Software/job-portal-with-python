from models import *
from schemas import *
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

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
        website=Or_profile.website
    )
    db.add(db_or_profile)
    db.commit()
    db.close()
    return db_or_profile
