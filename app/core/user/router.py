"""
The router for the user package.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import db
from app.core.user import schema as user_schema
from app.core.user.services import crud, auth, mail
from app.core.user.model import UserModel
from app.core.security.deps import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security.models import TokenModel
from app.core.user.services.roles import add_roles_to_user
from .services import password as password_service
from .services import mail as mail_service
from app.core.roles.schemas import AddRoles


router = APIRouter(
    tags=['users']
)


@router.post('/register', response_model=user_schema.User)
def register_user(*, database: Session = Depends(db.get_db), new_user: user_schema.UserCreate):
    """ Register new user

    Register new user by email and password.
    """
    existing_user = crud.get_by_email(db=database, email=new_user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='A user with the same email already exists.'
        )
    user_response = crud.create_user(db=database, new_user=new_user)
    if isinstance(user_response, dict):
        raise HTTPException(
            status_code=500,
            detail="Sorry, somethin went wrong. Please try again later."
        )
    return user_response


@router.post('/token', response_model=TokenModel)
async def login(*, database: Session = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log user in.
    """
    token = auth.user_login(db=database, email=form_data.username,
                            password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get('/me', response_model=user_schema.User)
def me(current_user: UserModel = Depends(get_current_user)):
    """Get currently authenticated user."""
    return current_user


@router.get('/email/verify/')
def verify_mail(token: str, db: Session = Depends(db.get_db)):
    """Verify email of a user."""
    email = mail.verify_email_token(token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail='Invalid token provided'
        )
    return crud.verify_email(email=email, db=db)


@router.get('/request-password-reset')
def request_password_reset(email: str, db: Session = Depends(db.get_db)):
    """Send email with token that let's user reset his/her password."""
    user = crud.get_by_email(db=db, email=email)
    # For security reasons we don't send error msg if the user does not exist.
    if not user:
        return True
    token = password_service.generate_password_reset_token(email)
    if not token:
        raise HTTPException(
            status_code=500,
            detail="Sorry, something went wrong. Please try again later."
        )
    mail_service.send_reset_password_email(
        email_to=email, token=token)
    return True


@router.post('/reset-password')
def reset_password(data: user_schema.ResetPassword, db: Session = Depends(db.get_db)):
    """Reset/Change password of unauthenticated user by providing a valid reset token."""
    email_from_token = password_service.verify_password_reset_token(data.token)
    if not email_from_token:
        raise HTTPException(
            status_code=400,
            detail='Invalid token'
        )
    if not email_from_token == data.email:
        raise HTTPException(
            status_code=400,
            detail='Invalid data'
        )
    updated_password = password_service.change_password(
        db=db, email=data.email, new_pass=data.new_password)
    if isinstance(updated_password, dict) and updated_password["error"]:
        raise HTTPException(
            status_code=400,
            detail=updated_password["msg"]
        )
    return True


@router.patch('/roles/add/{user_id}', response_model=user_schema.User)
def add_roles(user_id: str, data: AddRoles, db: Session = Depends(db.get_db)):
    """Add new roles to a user."""
    return add_roles_to_user(user_id=user_id, new_roles=data.roles, db=db)


@router.delete('/user/delete/{user_id}')
def delete_user(user_id: str, current_user: UserModel = Depends(get_current_user), db: Session = Depends(db.get_db)):
    """Delete a user."""
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to delete this user."
        )
    return crud.delete_user(db, user_id)
