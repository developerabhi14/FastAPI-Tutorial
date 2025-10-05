from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated,Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str, Field(...,description="Id of the patient", examples=['P001'])]
    name: Annotated[str, Field(...,description="Name of the patient")]
    age: Annotated[int, Field(..., gt=0,lt=120,description="Age of the patient")]
    gender: Annotated[Literal['male','female'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0,description="Height of the patient")]
    weight: Annotated[float, Field(..., gt=0,description="Weight of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]


    @computed_field
    @property
    def bmi(self)->float:
        return round((self.weight/(self.height**2)),2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Borderline"
        else:
            return "Obese"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male','female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "Fully Funcional API to manage patient records"}


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data=load_data()
    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # new patient add into database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into jsonn file
    save_data(data)
    return JSONResponse(status_code=201, content={'message':"Patient created successfully"})

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str= Path(...,title="Patient ID", description="The ID of the patient to view", example="P001")):
    """View patient by ID
    Example: Patient ID:P001
    """
    # load data
    data=load_data()
    # find patient by id
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")    

@app.get('/sort')
def sort_patient(sort_by: str=Query(..., title="Sort By", description="The field to sort patients by", example="age"), order: str=Query("asc", title="Order", description="The order to sort (asc or desc)", example="asc")):
    """Sort patients by a specific field
    Example: Sort By:age
    """
    valid_field=['height','weight', 'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_field)}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")
    # load data
    data=load_data()
    # sort data
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data
    
@app.put('/edit/{patient_id}')
def edit_patient(patient_id: str, patient: PatientUpdate):
    """Edit patient by ID
    Example: Patient ID:P001
    """
    # load data
    data=load_data()
    # find patient by id
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # update patient data
    stored_patient_data=data[patient_id]
    update_data=patient.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        stored_patient_data[key]=value
    stored_patient_data['id']=patient_id
    patient_obj=Patient(**stored_patient_data)
    stored_patient_data=patient_obj.model_dump(exclude=['id'])
    data[patient_id]=stored_patient_data


    # save data
    save_data(data)
    return JSONResponse(status_code=200, content={'message':"Patient updated successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    """Delete patient by ID
    Example: Patient ID:P001
    """
    # load data
    data=load_data()
    # find patient by id
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # delete patient data
    del data[patient_id]

    # save data
    save_data(data)
    return JSONResponse(status_code=200, content={'message':"Patient deleted successfully"})