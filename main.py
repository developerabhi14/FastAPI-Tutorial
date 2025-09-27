from fastapi import FastAPI, Path, HTTPException, Query
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
    