from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Query, Request,Form, status
from pydantic import BaseModel, EmailStr
from schemas import *
from config import *
from models import *
from crud import *
from io import BytesIO
from fastapi.responses import StreamingResponse
import PyPDF2
from fastapi.middleware.cors import CORSMiddleware

obj = UserModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Recruitment")

# Enable CORS to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/user/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: SessionLocal = Depends(get_db)):
    return create_user(db, user)

@app.post("/login/")
def login(login: Login, db: SessionLocal = Depends(get_db)):
    user = authenticate_user(db, login.email, login.password)
    if user.role == "job_seeeker":
        return {"email": user.email, "role": user.role, "profile_completion": user.profile_completion}
    else:
        return {"email": user.email, "role": user.role, "profile_completion": user.profile_completion}

@app.post("/job_seeker_profile/", response_model=JobSeekerProfileResponse)
def create_job_seeker_profile_endpoint(profile: JobSeekerProfileCreate, db: SessionLocal = Depends(get_db)):
    return create_job_seeker_profile(db, profile)


@app.post("/Organization_profile/", response_model=OrganizationProfileResponse)
def create_organization_profile_endpoint( profile: OrganizationProfileCreate, db: SessionLocal = Depends(get_db)):
    return create_organization_profile(db, profile)


@app.post("/upload/")
async def upload_files(
    user_email: str = Form(...),
    user_role: str = Form(...),
    profile_picture: UploadFile = File(...),
    resume: UploadFile = File(None),  # Optional file upload
    db: Session = Depends(get_db)
):
    # Allowed content types
    allowed_image_types = ["image/jpeg", "image/png", "image/jpg"]
    allowed_pdf_type = "application/pdf"
    max_file_size = 5 * 1024 * 1024  # 5 MB

    if user_role == "organization":
        # Organizations can only upload a profile picture (logo)
        if profile_picture.content_type not in allowed_image_types:
            raise HTTPException(status_code=400, detail="Invalid logo format. Only JPEG, PNG, JPG allowed.")

        # Read file content for the logo
        profile_picture_content = await profile_picture.read()
        if len(profile_picture_content) > max_file_size:
            raise HTTPException(status_code=400, detail="Logo size exceeds 5 MB.")

        # Save the logo (profile picture) in the database
        logo_record = FileModel(
            user_email=user_email,
            filename=profile_picture.filename,
            content_type=profile_picture.content_type,
            file_type="company_logo",
            file_content=profile_picture_content
        )
        db.add(logo_record)

    elif user_role == "job_seeker":
        # Job seekers must upload a profile picture, and optionally a resume
        if profile_picture.content_type not in allowed_image_types:
            raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG, PNG, JPG allowed.")

        # Read and save profile picture
        profile_picture_content = await profile_picture.read()
        if len(profile_picture_content) > max_file_size:
            raise HTTPException(status_code=400, detail="Profile picture size exceeds 5 MB.")

        profile_picture_record = FileModel(
            user_email=user_email,
            filename=profile_picture.filename,
            content_type=profile_picture.content_type,
            file_type="profile_picture",
            file_content=profile_picture_content
        )
        db.add(profile_picture_record)

        # If a resume is uploaded, validate and store it
        if resume:
            if resume.content_type != allowed_pdf_type:
                raise HTTPException(status_code=400, detail="Invalid resume format. Only PDF allowed.")

            resume_content = await resume.read()
            if len(resume_content) > max_file_size:
                raise HTTPException(status_code=400, detail="Resume size exceeds 5 MB.")

            resume_record = FileModel(
                user_email=user_email,
                filename=resume.filename,
                content_type=resume.content_type,
                file_type="resume",
                file_content=resume_content
            )
            db.add(resume_record)

    else:
        raise HTTPException(status_code=400, detail="Invalid user role. Must be 'job_seeker' or 'organization'.")

    # Commit changes to the database
    db.commit()

    return {"message": "Files uploaded successfully"}

@app.get("/files_download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    # Retrieve file from the database
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()  # Use FileModel

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    # Convert the file content (binary) into a streaming response
    file_like = BytesIO(db_file.file_content)

    # Set headers for downloading the file with its original name
    headers = {
        'Content-Disposition': f'attachment; filename="{db_file.filename}"'
    }

    # Return a StreamingResponse with the correct content type
    return StreamingResponse(file_like, media_type=db_file.content_type, headers=headers)


@app.get("/read/files/{file_id}")
async def read_file(file_id: int, db: Session = Depends(get_db)):
    # Retrieve file from the database
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    # Convert the file content (binary) into a BytesIO object
    file_like = BytesIO(db_file.file_content)

    # Try reading the file as text
    try:
        file_content = file_like.read().decode("utf-8")  # Decode as text
        return {"file_content": file_content}
    except UnicodeDecodeError:
        # Handle binary files like PDF
        file_like.seek(0)  # Reset to start for binary reading
        try:
            pdf_reader = PyPDF2.PdfReader(file_like)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return {"file_content": text}  # Return the extracted PDF content
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Unable to read file: {str(e)}")

@app.get("/open/resume/{file_id}")
async def open_resume(file_id: int, db: Session = Depends(get_db)):
    # Retrieve file from the database
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    # Ensure the content is in a BytesIO object
    file_like = BytesIO(db_file.file_content)
    file_like.seek(0)  # Reset the pointer to the start of the file

    # Setting appropriate headers for PDF
    headers = {
        "Content-Disposition": f'inline; filename="resume_{file_id}.pdf"'
    }

    # Return the StreamingResponse with the correct media type
    return StreamingResponse(file_like, media_type="application/pdf", headers=headers)


@app.post("/job_posts/")
def create_job_post(job_post: JobPostCreateSchema, db: Session = Depends(get_db)):
    job_post_detail = db.query(OrganizationProfileModel).filter(OrganizationProfileModel.user_email == job_post.email).first()
        # Check if user is an organization and profile is complete
    if job_post.role != "organization" or not job_post.profile_completion:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only organizations with complete profiles can post jobs"
        )
    # Create new job post
    new_job_post = JobPostModel(
        company_name = job_post_detail.company_name,
        posted_by=job_post.email,
        job_title=job_post.job_title,
        description=job_post.description,
        skills=job_post.skills,
        salary=job_post.salary,
        experience=job_post.experience,
        positions=job_post.positions,
        location=job_post.location,
        education=job_post.education
    )
    # Add and commit new job post to database
    db.add(new_job_post)
    db.commit()
    db.refresh(new_job_post)
    return new_job_post


@app.get("/jobs/")
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(JobPostModel).all()
    return jobs


@app.get("/posted_by_organization/")
def jobs_posted_by_organization(email: EmailStr, db: Session = Depends(get_db)):
    organization_jobs = db.query(JobPostModel).filter(JobPostModel.posted_by == email).all()
    if not organization_jobs:
        raise HTTPException(status_code=404, detail="No job posts found for this organization")
    return organization_jobs


@app.get("/jobs/{id}", response_model=JobPostResponseSchema)
def get_job_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    job = db.query(JobPostModel).filter(JobPostModel.job_id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")  
    return job

@app.post("/apply/")
def apply_to_job_endpoint(applicant: ApplicationCreateSchema, db: Session = Depends(get_db)):
    return apply_to_job(db, applicant)


@app.get("/get_applicants/")
def get_applicant_by_job_id(job_id: int, db: Session = Depends(get_db)):
    applicants = db.query(JobApplicationModel).filter(JobApplicationModel.job_id == job_id).all()
    return applicants

@app.put("/update_status")
def update_application_status(
    job_id: int, 
    job_seeker_email: EmailStr, 
    status_update: StatusUpdateRequest, 
    db: Session = Depends(get_db)
):
    # Retrieve the specific job application
    application = db.query(JobApplicationModel).filter(
        JobApplicationModel.job_id == job_id,
        JobApplicationModel.job_seeker_email == job_seeker_email
    ).first()
    # If no application is found, raise an exception
    if not application:
        raise HTTPException(status_code=404, detail="Job application not found")
    # Update the status of the application
    application.status = status_update.status
    # Commit the changes to the database
    db.commit()
    db.refresh(application)
    return {"message": "Application status updated successfully", "application": application}

