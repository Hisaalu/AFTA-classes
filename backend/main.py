from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import os
#from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_DIR, "../shared_data/savings.csv")

#print("📁 BACKEND SAVINGS PATH:", CSV_FILE)

#creating csv file
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns = ["user_id", "monthly_saving","start_date"])
    df.to_csv(CSV_FILE, index = False)

#pydantic models
class MonthlySavingsRequest(BaseModel):
    user_id: str
    monthly_saving: float

class LoanRequest(BaseModel):
    user_id: str

#saving the users yearly saving
@app.post("/save")
def save_monthly_plan(data: MonthlySavingsRequest):
    df = pd.read_csv(CSV_FILE)


    if data.user_id.strip() in df["user_id"].astype(str).str.strip().values:
        raise HTTPException(status_code = 400, detail= "User already registered.")
    
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
    print("📄 CSV Content:\n", df)

    user_row = df[df["user_id"] == data.user_id]

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
