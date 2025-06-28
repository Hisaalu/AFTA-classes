from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from fastapi import UploadFile, File
from pydantic import BaseModel
from datetime import datetime
from io import StringIO
import pandas as pd
import os

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://school-loan-backend.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#authentication routes
app.include_router(auth_router)

SHARED_DIR = "/tmp"
os.makedirs(SHARED_DIR, exist_ok=True)
CSV_FILE = os.path.join(SHARED_DIR, "savings.csv")

#creating csv file
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns = ["user_id", "monthly_saving","start_date"])
    df.to_csv(CSV_FILE, index = False)

#pydantic models
class User(BaseModel):
    username: str
    password: str   

class MonthlySavingsRequest(BaseModel):
    user_id: str
    monthly_saving: float

class LoanRequest(BaseModel):
    user_id: str

#registering new user
#@app.post("/register")
#def register_user(user: User):
    #return {"message": f"User {user.username} registered successfully"}

#saving the users monthly saving plan
@app.post("/save")
def save_monthly_plan(data: MonthlySavingsRequest):
    df = pd.read_csv(CSV_FILE)

    user_id = data.user_id.strip().lower()
    df["user_id"] = df["user_id"].astype(str).str.strip().str.lower()

    if user_id in df["user_id"].values:
        raise HTTPException(status_code=400, detail="User already registered.")
    
    new_entry = pd.DataFrame([{
        "user_id": data.user_id.strip(),
        "monthly_saving": data.monthly_saving,
        "start_date": datetime.today().strftime('%Y-%m-%d')
    }])

    df = pd.concat([df, new_entry], ignore_index = True)
    df.to_csv(CSV_FILE, index=False)

    return {"message": "Saved successfully", "start_date": new_entry.iloc[0]["start_date"]}


# Calculates and returns loan amount
@app.post("/loan")
def calculate_loan(data: LoanRequest):
    df = pd.read_csv(CSV_FILE)
    user_id = data.user_id.strip().lower()

    user_row = df[df["user_id"].astype(str).str.strip().str.lower() == user_id]

    if user_row.empty:
        raise HTTPException(status_code=404, detail="User not found.")
    
    monthly = float(user_row["monthly_saving"].values[0])
    start_date = datetime.strptime(user_row["start_date"].values[0], '%Y-%m-%d')
    today = datetime.today()
    months_saved = (today.year - start_date.year) * 12 + (today.month - start_date.month)
    months_saved = max(1, months_saved)

    total_saved = monthly * months_saved
    loan_amount = total_saved * 2
    
     
    return {
        "user_id": data.user_id,
        "months_saved": months_saved,
        "total_saved": total_saved,
        "loan_eligible_amount": loan_amount,
        "start_date": start_date.date()
        }

# Expose CSV for download
@app.get("/csv")
def get_csv():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, detail="CSV not found.")
    
    with open(CSV_FILE, "r") as f:
        content = f.read()

    return Response(content=content, media_type="text/csv")

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    contents = await file.read()
    try:
        new_df = pd.read_csv(StringIO(contents.decode("utf-8")))

        # Ensuring required columns exist
        required_columns = {"user_id", "monthly_saving", "start_date"}
        if not required_columns.issubset(new_df.columns):
            raise HTTPException(status_code=400, detail=f"CSV must include columns: {required_columns}")

        # Parsing and cleaning start_date
        new_df["start_date"] = pd.to_datetime(new_df["start_date"], errors="coerce")
        new_df = new_df.dropna(subset=["start_date"])
        new_df["start_date"] = new_df["start_date"].dt.strftime('%Y-%m-%d')

        # Lowercase and strip user_ids
        new_df["user_id"] = new_df["user_id"].astype(str).str.strip().str.lower()

        # Checking for duplicates within the uploaded file
        if new_df["user_id"].duplicated().any():
            raise HTTPException(status_code=400, detail="Uploaded CSV contains duplicate user IDs.")
        
        # Saving to CSV
        new_df.to_csv(CSV_FILE, index=False)
        return {"message": "CSV uploaded and saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {e}")
