from fastapi import APIRouter, HTTPException
from src.utils.error import Missing, Duplicate
import  src.service.user as service
from src.schemas.user import UserOut, UserCreate, UserUpdate
from settings import settings

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('', response_model=list[UserOut])
@router.get('/', response_model=list[UserOut])
def get_all() -> list[UserOut]:
    return service.get_all()


@router.get('/{id}', response_model=UserOut)
def get_one(id: str) -> UserOut:
    try:
        return service.get_one(id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post('', status_code=201, response_model=UserOut)
@router.post('/', status_code=201, response_model=UserOut)
def create_user(data: UserCreate) -> UserOut:
    try:
        return service.create_user(data)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    

@router.patch('', response_model=UserOut)
@router.patch('/', response_model=UserOut)
def modify_user(data: UserUpdate) -> UserOut:
    try:
        return service.modify_user(data)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)