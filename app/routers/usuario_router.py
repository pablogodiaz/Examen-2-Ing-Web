from typing import List
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from model import Usuario
from model import UsuarioUpdate
from model import Contacto

router = APIRouter()

'''CREAR USUARIO'''
@router.post("/", response_description="Crear usuario", status_code=status.HTTP_201_CREATED, response_model=Usuario)
def create_user(request: Request, Usuario: Usuario = Body(...)):

    Usuario = jsonable_encoder(Usuario)
    
    new_usuario = request.app.database["usuario"].insert_one(Usuario)
    created_usuario = request.app.database["usuario"].find_one(
        {"_id": new_usuario.inserted_id}
    )
    
    return created_usuario


'''LISTAR USUARIOS'''
@router.get("/list_all",response_description="List all users", response_model=List[Usuario])
def list_users(request: Request):
    usuarios = list(request.app.database["usuario"].find(limit=100))
    return usuarios

'''GET USUARIO'''
@router.get("/{telefono}", response_description="Get a single user", response_model=Usuario)
def get_user(telefono:int, request: Request):
    if(usuario := request.app.database["usuario"].find_one({"telefono":telefono})):
        return usuario

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con telefono {telefono} not found")

'''UPDATE USUARIO '''
@router.put("/{telefono}", response_description="Actualizar un usuario", response_model=Usuario)
def update_user(telefono: int, request: Request, usuario: UsuarioUpdate = Body(...)):
    usuario = {k: v for k, v in usuario.dict().items() if v is not None}

    if len(usuario) >= 1:
        update_result = request.app.database["usuario"].update_one(
            {"telefono": telefono}, {"$set": usuario}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con telefono {telefono} no encontrado")

    if (
        existing_usuario := request.app.database["usuario"].find_one({"telefono":telefono})
    ) is not None:
        return existing_usuario

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con telefono {telefono} no encontrado")

'''DELETE USUARIO'''
@router.delete("/{telefono}", response_description="Borrar usuario")
def delete_user(telefono:int,request: Request, response: Response):
    usuario_deleted = request.app.database["usuario"].delete_one({"telefono": telefono})

    if usuario_deleted.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con telefono {telefono} no encontrado")

'''El CRUD de contactos esta dentro del CRUD de usuario'''

'''GET POR ALIAS'''
@router.get("/{alias}", response_description="Get a single user", response_model=Usuario)
def get_user_by_alias(alias:str, request: Request):
    if(usuario := request.app.database["usuario"].find_one({"alias":alias})):
        return usuario

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con telefono {alias} not found")