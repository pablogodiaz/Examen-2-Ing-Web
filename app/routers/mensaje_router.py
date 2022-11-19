from typing import List
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from model import Mensaje
from model import MensajeUpdate

router = APIRouter()

'''CREAR MENSAJE'''
@router.post("/", response_description="Crear mensaje", status_code=status.HTTP_201_CREATED, response_model=Mensaje)
def create_message(request: Request, Mensaje: Mensaje = Body(...)):

    Mensaje = jsonable_encoder(Mensaje)
    
    new_mensaje = request.app.database["mensaje"].insert_one(Mensaje)
    created_mensaje = request.app.database["mensaje"].find_one(
        {"_id": new_mensaje.inserted_id}
    )
    
    return created_mensaje


'''LISTAR MENSAJES'''
@router.get("/",response_description="Lista de mensajes", response_model=List[Mensaje])
def list_messages(request: Request):
    mensajes = list(request.app.database["mensaje"].find(limit=100))
    return mensajes

'''GET MENSAJE'''
@router.get("/{id}", response_description="Get un mensaje", response_model=Mensaje)
def get_message(id:str, request: Request):
    if(mensaje := request.app.database["mensaje"].find_one({"id":id})):
        return mensaje

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensaje con id {id} not found")

'''UPDATE MENSAJE '''
@router.put("/{id}", response_description="Actualizar un mensaje", response_model=Mensaje)
def update_message(id: str, request: Request, mensaje: MensajeUpdate = Body(...)):
    mensaje = {k: v for k, v in mensaje.dict().items() if v is not None}

    if len(mensaje) >= 1:
        update_result = request.app.database["mensaje"].update_one(
            {"id": id}, {"$set": mensaje}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensaje con id {id} no encontrado")

    if (
        existing_mensaje := request.app.database["mensaje"].find_one({"id":id})
    ) is not None:
        return existing_mensaje

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensaje con id {id} no encontrado")

'''DELETE MENSAJE'''
@router.delete("/{id}", response_description="Borrar mensaje")
def delete_message(id:str,request: Request, response: Response):
    mensaje_deleted = request.app.database["mensaje"].delete_one({"id": id})

    if mensaje_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensaje con id {id} no encontrado")

'''GET MENSAJES DE UN USUARIO A OTRO'''
@router.get("/{telefono1}/{telefono2}", response_description="Get mensajes", response_model=List[Mensaje])
def get_messages_between_users(telefono1, telefono2:int, request: Request):
    if(mensajes := request.app.database["mensaje"].find({"$and": [{"origen": telefono1}, {"destino": telefono2}]})):
        return mensajes

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensajes entre usuarios con telefono {telefono1} y {telefono2} no encontrados")

'''GET MENSAJES POR BUSQUEDA CON PARTE DEL TEXTO'''
@router.get("/busqueda/{telefono}/{busqueda}", response_description="Get mensajes", response_model=List[Mensaje])
def get_message_by_text(busqueda:str, telefono:int, request: Request):
    if(mensajes := request.app.database["mensaje"].find({"texto": "/" + busqueda + "/", "$or": [{"origen": telefono}, {"destino": telefono}]})):
        return mensajes

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Mensajes con texto {busqueda} no encontrado")