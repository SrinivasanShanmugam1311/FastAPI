from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="SIP Calculator API")

# Request model
class SIPRequest(BaseModel):
    monthly: float    # ₹ per month
    rate: float       # Annual %, non-negative
    years: float      # Time in years, > 0

# Function to compute SIP
def compute_sip(monthly: float, rate: float, years: float):
    r = (rate / 100.0) / 12.0
    n = int(years * 12)

    if r == 0:
        fv = monthly * n
    else:
        fv = monthly * (((1 + r) ** n - 1) / r) * (1 + r)

    invested = monthly * n
    gain = fv - invested
    return round(invested, 2), round(fv, 2), round(gain, 2)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to SIP Calculator API. Use /sip endpoint."}

# GET method with query params
@app.get("/sip")
def get_sip(
    monthly: float = Query(..., gt=0),
    rate: float = Query(..., ge=0),
    years: float = Query(..., gt=0),
):
    print("GET method before compute_sip()")
    invested, future_value, gain = compute_sip(monthly, rate, years)
    print("GET method after compute_sip()")
    return {
        "monthly": monthly,
        "rate": rate,
        "years": years,
        "invested": invested,
        "future_value": future_value,
        "gain": gain,
    }

# POST method with JSON body
@app.post("/sip")
def post_sip(data: SIPRequest):
    print("POST method before compute_sip()")
    invested, future_value, gain = compute_sip(data.monthly, data.rate, data.years)
    print("POST method after compute_sip()")
    return {
        "monthly": data.monthly,
        "rate": data.rate,
        "years": data.years,
        "invested": invested,
        "future_value": future_value,
        "gain": gain,
    }
