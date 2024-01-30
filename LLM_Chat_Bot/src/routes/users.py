import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas import UserResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET endpoint that returns the current user's information.

    :param current_user: User: Get the current user
    :return: The current user object, which is a user instance
    """
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        The function takes in an UploadFile object, which is a file that has been uploaded to the server.
        It also takes in a User object and Session object as dependencies.

        The function first configures cloudinary with our cloudinary account information, then uploads the file to
            our RestChat folder on Cloudinary using its public_id (which is set to be equal to RestChat/username).

    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the repository function
    :return: A user object, but the avatar is not updated in the database
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'RestChat/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'RestChat/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
