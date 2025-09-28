from pydantic import BaseModel

class Patient(BaseModel):
    name:str
    age:int
    weight:float


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted into database")

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Updated into database")

patient_info={'name':'John Doe', 'age':30, 'weight':'70.5'}

patient1=Patient(**patient_info)

insert_patient_data(patient1)

patient_info={'name':'John Doe', 'age':30, 'weight':"86"}

update_patient_data(patient1)