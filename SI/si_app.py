from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Simple Interest Calculator API")

# Request model
class SIRequest(BaseModel):
    principal: float  # ₹
    rate: float       # Annual %, non-negative
    years: float      # Time in years, > 0

# Function to compute Simple Interest
def compute_simple_interest(principal: float, rate: float, years: float):
    si = (principal * rate * years) / 100.0
    amount = principal + si
    return round(si, 2), round(amount, 2)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Simple Interest Calculator API. Use /si endpoint."}

# GET method with query params
@app.get("/si")
def get_si(
    principal: float = Query(..., gt=0),
    rate: float = Query(..., ge=0),
    years: float = Query(..., gt=0),
):
    print("GET method before compute_simple_interest()")
    si, amount = compute_simple_interest(principal, rate, years)
    print("GET method after compute_simple_interest()")
    return {
        "principal": principal,
        "rate": rate,
        "years": years,
        "simple_interest": si,
        "amount": amount,
    }

# POST method with JSON body
@app.post("/si")
def post_si(data: SIRequest):
    print("POST method before compute_simple_interest()")
    si, amount = compute_simple_interest(data.principal, data.rate, data.years)
    print("POST method after compute_simple_interest()")
    return {
        "principal": data.principal,
        "rate": data.rate,
        "years": data.years,
        "simple_interest": si,
        "amount": amount,
    }
