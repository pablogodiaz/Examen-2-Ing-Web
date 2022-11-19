from typing import List
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from model import Example

router = APIRouter()

'''CREATE EXAMPLE'''
@router.post("/", response_description="Create example", status_code=status.HTTP_201_CREATED, response_model=Example)
def create_household(request: Request, Example: Example = Body(...)):

    Example = jsonable_encoder(Example)
    
    new_example = request.app.database["example"].insert_one(Example)
    created_example = request.app.database["example"].find_one(
        {"_id": new_example.inserted_id}
    )
    
    return created_example


'''LIST EXAMPLES'''
@router.get("/",response_description="List all examples", response_model=List[Example])
def list_bookings(request: Request):
    examples = list(request.app.database["example"].find(limit=100))
    return examples

'''GET EXAMPLE'''
@router.get("/{id}", response_description="Get a single example", response_model=Example)
def get_booking(id:str, request: Request):
    if(example := request.app.database["example"].find_one({"id":id})):
        return example

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Example with ID {id} not found")