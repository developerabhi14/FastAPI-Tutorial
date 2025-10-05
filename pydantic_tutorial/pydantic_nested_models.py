from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address: Address

address_dict={'city':'Gurgaon', 'state':"Haryana", 'pin':"231123"}

address1=Address(**address_dict)

patient_dict={'name':'abhi', 'gender':'male','age':'32','address':address1}

patient1=Patient(**patient_dict)

print(patient_dict)
print(patient1.address.city)