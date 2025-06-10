from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow access to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    savings: float

@app.post("/calculate-loan")
def calculate_loan(data: LoanRequest):
    multiplier = 3 
    loan_amount = data.savings * multiplier
    return {"loan_amount": round(loan_amount, 2)}
