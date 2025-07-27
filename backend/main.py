from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
import shutil
import os
import models  # your SQLAlchemy models (User, etc.)
from database import SessionLocal, engine
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# JWT Configurations
SECRET_KEY = "YOUR_SUPER_SECRET_KEY"  # replace with a strong secret in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Utility functions

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Pydantic Models

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str


class TaxRequest(BaseModel):
    income: float


# Database session dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables if not exist
models.Base.metadata.create_all(bind=engine)


# Routes

@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = models.User(email=user.email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}


@app.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/protected-route")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"email": current_user.email, "msg": "This is a protected route"}


def calculate_income_tax(income: float) -> float:
    if income <= 250000:
        return 0.0
    elif income <= 500000:
        return (income - 250000) * 0.05
    elif income <= 1000000:
        return (250000 * 0.05) + (income - 500000) * 0.20
    else:
        return (250000 * 0.05) + (500000 * 0.20) + (income - 1000000) * 0.30


@app.post("/calculate-tax")
def calculate_tax(request: TaxRequest):
    tax = calculate_income_tax(request.income)
    return {"income": request.income, "tax": tax}


@app.post("/upload-document/")
async def upload_document(
    user_id: int,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    file_location = os.path.join(uploads_dir, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = models.Document(
        user_id=user_id,
        file_path=file_location,
        document_type=document_type,
        parsed_data=None
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"id": new_doc.id, "file_path": file_location, "document_type": document_type}
