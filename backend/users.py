from fastapi import APIRouter, HTTPException
import models, schemas, utils

router = APIRouter()

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    if models.User.objects(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed_pw, role=user.role)
    new_user.save()
    return schemas.UserOut(id=str(new_user.id), username=new_user.username, role=new_user.role)

@router.get("/", response_model=list[schemas.UserOut])
def get_users():
    users = models.User.objects()
    return [schemas.UserOut(id=str(u.id), username=u.username, role=u.role) for u in users]
