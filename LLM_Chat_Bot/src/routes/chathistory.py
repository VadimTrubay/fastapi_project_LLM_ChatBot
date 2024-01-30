from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.conf import messages
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import chathistory as repository_history
from src.schemas import ChatHistoryBase, ChatHistoryModel
from src.services.auth import auth_service
from src.services.role import RoleAccess

router = APIRouter(prefix='/history', tags=["history"])

allowed_get_history = RoleAccess([Role.admin, Role.moderator, Role.user])  # noqa
allowed_add_messages = RoleAccess([Role.user, Role.admin])  # noqa


@router.post("/{chat_id}", response_model=ChatHistoryModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_add_messages)])
async def create_message(chat_id: int, body: ChatHistoryBase, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The **create_chat** function creates a new chat for the user with the given id.

    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A chat object, which is then serialized as json
    """
    new_message = await repository_history.create_message(chat_id, body, db, current_user)
    return new_message


@router.get("/{chat_id}", response_model=List[ChatHistoryModel], dependencies=[Depends(allowed_get_history)])
async def get_history(chat_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The **get_chat** function returns a specified chat from the database.

    :param chat_id: int: Pass the chat id to the function
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: The chat object
    """
    history = await repository_history.get_history_by_chat(chat_id, db)
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.CHAT_NOT_FOUND)
    return history
