from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
#from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#temporary in memory storage
savings_data = {}

#pydantic models
class MonthlySavingsRequest(BaseModel):
    user_id: str
    monthly_saving: float

class LoanRequest(BaseModel):
    user_id: str

#saving the users yearly saving
@app.post("/save")
def save_monthly_saving(data: MonthlySavingsRequest):
    if data.user_id in savings_data:
        raise HTTPException(status_code = 400, deatail= "Saving already recorded for this user.")
    
    savings_data[data.user_id] = {
        "monthly_saving": data.monthly_saving,
        "start_date": datetime.today().strftime('%Y-%m-%d') 
        }

    return {
        "message": f"Saving plan of UGX {data.monthly_saving:,.0f}/month recorded.",
        "start_date": savings_data[data.user_id]["start_date"]
        }

# Calculate and return loan amount
@app.post("/loan")
def calculate_loan(data: LoanRequest):
    user_info = savings_data.get(data.user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found.")
    

    start_date = datetime.strptime(user_info["start_date"], '%Y-%m-%d')
    today = datetime.today()

    months_saved = (today.year - start_date.year) * 12 + (today.month - start_date.month)
    months_saved = max(1, months_saved)

    monthly_saving = user_info["monthly_saving"]
    total_saved = monthly_saving * months_saved
    loan_amount = total_saved * 2
    
     
    return {
        "user_id": data.user_id, 
        "start_date": user_info["start_date"],
        "months_saved": months_saved,
        "total_saved": total_saved,
        "loan_eligible_amount": loan_amount
        }
