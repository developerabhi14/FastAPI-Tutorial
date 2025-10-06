from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated,Literal, Optional
import pickle
import pandas as pd

with open("model.pkl", "rb") as f:
    model=pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# pudantic model to validate incoming data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the person", examples=[25])]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg", examples=[70.5])]
    height:Annotated[float, Field(..., gt=0, description="Height in meters", examples=[1.75])]
    income_lpa:Annotated[float, Field(..., gt=0, description="Income in LPA", examples=[5.5])]
    smoker:Annotated[bool, Field(..., description="Whether the person is a smoker or not")]
    city:Annotated[str, Field(..., description="City where the person lives")]
    occupation:Annotated[Literal['retired','freelancer','student','government_job', 'business_owner','unemployed','private_job'], Field(..., description="Occupation of the person")]

    @computed_field
    @property
    def bmi(self)->float:
        return round((self.weight/(self.height**2)),2)
    
    @computed_field
    @property
    def lifestyle_risk(self)-> str:
        if self.smoker and self.bmi>30:
            return "high"
        elif self.smoker or self.bmi>27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self)-> str:
        if self.age<25:
            return "young"
        elif self.age<45:
            return "adult"
        elif self.age<60:
            return "middle_aged"
        else:
            return "senior"
        
    @computed_field
    @property
    def city_tier(self)-> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def predict_insurance_premium(input_data: UserInput):
    # convert to dataframe
    data=pd.DataFrame([input_data.model_dump()])
    print(data)
    # make prediction
    prediction=model.predict(data)[0]
    return JSONResponse(status_code=200, content={"predicted_insurance_premium": prediction})
