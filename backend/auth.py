from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import pandas as pd
import os

router = APIRouter()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SHARED_DIR = "/tmp"
CSV_FILE = os.path.join(SHARED_DIR, "users.csv")
os.makedirs(SHARED_DIR, exist_ok=True)

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["username", "hashed_password"]).to_csv(CSV_FILE, index=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_user(username: str):
    df = pd.read_csv(CSV_FILE)
    user = df[df["username"] == username]
    if not user.empty:
        return {"username": username, "hashed_password": user.iloc[0]["hashed_password"]}
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return None
    if not pwd_context.verify(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: RegisterRequest):
    df = pd.read_csv(CSV_FILE)
    if user.username in df["username"].values:
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed = pwd_context.hash(user.password)
    df.loc[len(df)] = [user.username, hashed]
    df.to_csv(CSV_FILE, index=False)
    return {"message": "User registered successfully."}

print("✅ users.csv now contains:")
print(pd.read_csv(CSV_FILE))


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
