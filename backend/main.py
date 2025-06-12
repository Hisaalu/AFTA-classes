from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#temporary in memory storage
savings_data = {}

# Allow access to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#pydantic models
class SavingsRequest(BaseModel):
    user_id: str
    monthly_saving: float

class LoanRequest(BaseModel):
    user_id: str

#saving the users monthly saving
@app.post("/save")
def save_amount(data: SavingsRequest):
    if data.user_id in savings_data:
        raise HTTPException(status_code = 400, deatail= "Saving already recorded for this user.")
    savings_data[data.user_id] = data.Monthly_saving
    return {"message": "Savings recorded successfully."}

# Calculate and return loan amount
@app.post("/loan")
def calculate_loan(data: LoanRequest):
    if data.user_id not in savings_data:
        raise HTTPException(status_code=404, detail="No savings found for this user.")
    
    saving = savings_data[data.user_id]
    loan_amount = saving * 2 
    return {"user_id": data.user_id, "loan_eligible_amount": loan_amount}
