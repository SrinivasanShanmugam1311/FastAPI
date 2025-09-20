
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="BMI Calculator API")

# Request model
class BMIRequest(BaseModel):
    weight: float  # in kg
    height: float  # in cm

# Function to calculate BMI
def calculate_bmi(weight: float, height: float) -> float:
    height_m = height / 100  # convert cm → meters
    return round(weight / (height_m ** 2), 2)

# Function to categorize BMI
def bmi_category(bmi: float) -> str:
    if bmi < 16:
        return "Severe Thinness"
    elif bmi < 17:
        return "Moderate Thinness"
    elif bmi < 18.5:
        return "Mild Thinness"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    elif bmi < 35:
        return "Obese Class I"
    elif bmi < 40:
        return "Obese Class II"
    else:
        return "Obese Class III"

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to BMI Calculator API. Use /bmi endpoint."}

# GET method with query params
@app.get("/bmi")
def get_bmi(weight: float = Query(..., gt=0), height: float = Query(..., gt=0)):
    print("this is the get method called before calculate_bmi(weight, height)")
    bmi = calculate_bmi(weight, height)
    print("this is the get method called after calculate_bmi(weight, height)")
    return {"weight": weight, "height": height, "bmi": bmi, "category": bmi_category(bmi)}

# POST method with JSON body
@app.post("/bmi")
def post_bmi(data: BMIRequest):
    print("this is the post method called before calculate_bmi(weight, height)")
    bmi = calculate_bmi(data.weight, data.height)
    print("this is the post method called after calculate_bmi(weight, height)")
    return {"weight": data.weight, "height": data.height, "bmi": bmi, "category": bmi_category(bmi)}
