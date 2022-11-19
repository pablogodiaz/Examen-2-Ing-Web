from datetime import date, datetime
from lib2to3.pgen2.token import OP
import uuid
from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from typing import List, Optional
from datetime import date

class Date(BaseModel):
    date: datetime = Field(alias="$date", default=datetime.now())

class Contacto(BaseModel):
    telefono: int
    alias: str

    @validator("telefono")
    def check_telefono_valido(cls, v):
        if v > 999999999 or v < 100000000:
            raise ValueError("Telefono invalido")
        return v

class Usuario(BaseModel):
    telefono: int
    alias: str
    contactos: List[Contacto]

    @validator("telefono")
    def check_telefono_valido(cls, v):
        if v > 999999999 or v < 100000000:
            raise ValueError("Telefono invalido")
        return v     

class UsuarioUpdate(BaseModel):
    telefono: Optional[int]
    alias: Optional[str]
    contactos: Optional[List[Contacto]]

    @validator("telefono")
    def check_telefono_valido(cls, v):
        if v > 999999999 or v < 100000000:
            raise ValueError("Telefono invalido")
        return v

class Mensaje(BaseModel):
    id: str
    timestamp: Date
    origen: int
    destino: int
    texto: str

    @validator("texto")
    def caracteres_menor_400(cls, v):
        if len(v) > 400:
            raise ValueError("Longitud supera 400 caracteres")
        return v

class MensajeUpdate(BaseModel):
    timestamp: Optional[Date]
    origen: Optional[int]
    destino: Optional[int]
    texto: Optional[str]

    @validator("texto")
    def caracteres_menor_400(cls, v):
        if len(v) > 400:
            raise ValueError("Longitud supera 400 caracteres")
        return v