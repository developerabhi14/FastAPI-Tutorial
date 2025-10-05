from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
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

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains=['hdfc.com','icici.com']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value
    
    @field_validator('name') # default mode=after
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0<value<100:
            return value
        raise ValueError("Age must be between 1 and 99")
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact_detail:
            raise ValueError("Emergency contact is required for patients above 60 years")
        return model
    

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Updated into database")

patient_info={'name':'John Doe', 'website':'https://www.abi.com','email':'ac@hdfc.com','age':'78', 'weight':70.5, 'married':False, 'allergies':['pollen', "nuts"], 'contact_detail':{'emergency':'12332532','email':'abhi@gmail.com'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)

patient_info={'name':'John Doe', 'website':'https://www.abi.com','email':'ac@icici.com', 'age':30, 'weight':86,  'allergies':['pollen', "nuts"],'contact_detail':{'email':'abhi@gmail.com'}}

patient1=Patient(**patient_info) # validation performed here

update_patient_data(patient1)