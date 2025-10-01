from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated
class Patient(BaseModel):
    name:str=Annotated[str, Field(max_length=50, title="name of the patient",description="Full name of the patient", examples=["Abhishek"], default="John Doe")]
    # name:str=Field(max_length=50, )
    age:int=Field(gt=0, lt=120)
    email:EmailStr
    website:AnyUrl
    weight:Annotated[float,Field(gt=0, strict=True, description="Weight in kg")]
    married:bool=False
    allergies: Annotated[Optional[List[str]],Field(max_length=5, description="List of allergies", default=None)]
    contact_detail: Dict[str, str]


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Updated into database")

patient_info={'name':'John Doe', 'website':'https://www.abi.com','email':'ac@gmail.com','age':30, 'weight':70.5, 'married':False, 'allergies':['pollen', "nuts"], 'contact_detail':{'email':'abhi@gmail.com'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)

patient_info={'name':'John Doe', 'website':'https://www.abi.com','email':'ac@gmail.com', 'age':30, 'weight':86,  'allergies':['pollen', "nuts"],'contact_detail':{'email':'abhi@gmail.com'}}

patient1=Patient(**patient_info)

update_patient_data(patient1)