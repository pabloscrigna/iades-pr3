# Ejercicio discos

# coleccion discos
# Album - Autor - titulos

# coleccion: Autor
# Nombre - apellido - nacionalidad


from datetime import datetime, timezone
from pymongo import MongoClient
from pydantic import BaseModel, Field


class Disco(BaseModel):
    album: str
    autor: str
    creado: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))

    def to_bson(self):
        data = self.model_dump()
        data["creado"] = data.get("creado").isoformat()
        
        return data


class Autor(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: str

    # Convert the Pydantic model into a dictionary compatible with MongoDB
    def to_bson(self):
        return self.model_dump()


url = "mongodb://localhost:27017"

try:

    db = MongoClient(url)
    db.server_info()

except Exception as e:
    print(e)
    exit(1)

print("Esta corriendo")

# Base de datos
db = db["discografica"]

# Colecciones
db_discos = db["discos"]
db_autor = db["autores"]


autor = Autor(nombre="autor_nombre1", apellido="autor_apellido_sin_key", nacionalidad="autor_nac")
disco = Disco(album="Paranoia", autor="Garnica")

print(autor)

print(disco)

# print(disco.to_bson())
# db_autor.insert_one(autor.to_bson())

db_discos.insert_one(disco.to_bson())