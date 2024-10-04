

from pydantic import BaseModel 
from typing import List
from pymongo import MongoClient
from bson import ObjectId


class Accesorio(BaseModel):
    sku: str
    precio: float
    nombre: str
    marca: str
    compatible: List[str]

    def to_bson(self):

        data = self.model_dump()

        return data
    

# Init DB
url = "mongodb://localhost:27017"

try:

    db = MongoClient(url)
    db.server_info()

except Exception as e:
    print(e)
    exit(1)

db = db["Gringo"]
db = db["accesorios"]

print("Esta corriendo")


#1 Insert de un accesorio

accesorio = Accesorio(
    sku="ABZ-153",
    nombre="tuercas",
    marca="VW",
    precio=167.67,
    compatible=[]
)

doc = db.insert_one(accesorio.to_bson())

print(doc.inserted_id)


# 2. Leer en la DB

accesorio_doc = db.find()

for acc in accesorio_doc:
    print(acc)

# 3. leer id

query = {"_id": ObjectId(doc.inserted_id)}
accesorio_doc = db.find_one(query)

print(f"Accesorio {doc.inserted_id} : {accesorio_doc}")

# 4. delete
query_delete = {"sku": "ABZ-153"}

delete_doc = db.delete_many(query_delete)

print(delete_doc.deleted_count)

# 5. update

query_update = {"sku": "ABC-123"}

update_doc = db.update_many(query_update, {"$set" : { "compatible": ["VW"]} })

print(update_doc.modified_count)