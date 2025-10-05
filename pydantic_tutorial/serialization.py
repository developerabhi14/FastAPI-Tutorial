from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str ='Male'
    age:int
    address: Address

address_dict={'city':'Gurgaon', 'state':"Haryana", 'pin':"231123"}

address1=Address(**address_dict)

patient_dict={'name':'abhi','age':'32','address':address1}

patient1=Patient(**patient_dict)
# you can control which fields you want to export
# temp=patient1.model_dump()
temp=patient1.model_dump(include=['name','gender'])
print("***************\n")
print(temp)
print(type(temp))
# exclude unset--> ignore default value if not set
temp=patient1.model_dump_json(exclude={'name':...,'address':{'state':...}}, exclude_unset=True)

print("***************\n")
print(temp)
print(type(temp))