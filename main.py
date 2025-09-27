from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

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
