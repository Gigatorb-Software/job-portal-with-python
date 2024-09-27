from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Query
from pydantic import BaseModel
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
    return {"email": user.email}

@app.post("/job_seeker_profile/")
def create_job_seeker_profile_endpoint(profile: JobSeekerProfileCreate, resume: UploadFile = File(), profile_pic: UploadFile = File(), db: SessionLocal = Depends(get_db)):
    return create_job_seeker_profile(db, profile, resume, profile_pic)

@app.post("/Organization_profile/")
def create_organization_profile_endpoint( profile: OrganizationProfileCreate, logo: UploadFile, db: SessionLocal = Depends(get_db)):
    return create_organization_profile(db, profile, logo)


@app.post("/uploadfile/")
async def upload_file(
    user_id: int,  # Accept user_id to associate the files
    db: Session = Depends(get_db), 
    resume: UploadFile = File(...),  # For PDF resumes
    profile_pic: UploadFile = File(...)  # For images (JPEG, PNG, JPG)
):
    # Read the resume content as binary
    resume_content = await resume.read()
    
    # Save the resume in the database
    db_resume = FileModel(
        user_id=user_id,  # Associate with user
        filename=resume.filename,
        content_type=resume.content_type,
        file_content=resume_content,
        file_type="resume"
    )
    db.add(db_resume)

    # Read the profile picture content as binary
    profile_pic_content = await profile_pic.read()
    
    # Save the profile picture in the database
    db_profile_pic = FileModel(
        user_id=user_id,  # Associate with user
        filename=profile_pic.filename,
        content_type=profile_pic.content_type,
        file_content=profile_pic_content,
        file_type="profile_pic"
    )
    db.add(db_profile_pic)

    # Commit both attachments to the database
    db.commit()
    
    # Refresh to get updated records
    db.refresh(db_resume)
    db.refresh(db_profile_pic)

    return {
        "resume": {"filename": db_resume.filename, "file_type": db_resume.file_type},
        "profile_pic": {"filename": db_profile_pic.filename, "file_type": db_profile_pic.file_type}
    }

@app.get("/files/{file_id}")
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