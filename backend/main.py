from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Query, Request
from pydantic import BaseModel, EmailStr
from schemas import *
from config import *
from models import *
from crud import *
from io import BytesIO
from fastapi.responses import StreamingResponse
import PyPDF2

obj = UserModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Recruitment")

@app.post("/user/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: SessionLocal = Depends(get_db)):
    return create_user(db, user)

@app.post("/login/")
def login(login: Login, db: SessionLocal = Depends(get_db)):
    user = authenticate_user(db, login.email, login.password)
    if user.role == "job_seeeker":
        return {"email": user.email, "role": user.role}
    else:
        return {"email": user.email, "role": user.role}

@app.post("/job_seeker_profile/", response_model=JobSeekerProfileResponse)
def create_job_seeker_profile_endpoint(profile: JobSeekerProfileCreate, db: SessionLocal = Depends(get_db)):
    return create_job_seeker_profile(db, profile)

@app.post("/Organization_profile/")
def create_organization_profile_endpoint( profile: OrganizationProfileCreate, db: SessionLocal = Depends(get_db)):
    return create_organization_profile(db, profile)


@app.post("/upload/")
async def upload_files(
    user_email: str, 
    user_role: str,  
    request: Request, 
    db: Session = Depends(get_db)
):
    # Allowed content types
    allowed_image_types = ["image/jpeg", "image/png", "image/jpg"]
    allowed_pdf_type = "application/pdf"
    max_file_size = 5 * 1024 * 1024  # 5 MB

    form = await request.form()
    profile_picture: UploadFile = form.get("profile_picture")
    resume: Optional[UploadFile] = form.get("resume")

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