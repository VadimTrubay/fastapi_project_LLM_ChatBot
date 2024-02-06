# from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
# from sqlalchemy.orm import Session
# from typing import List
#
# from src.database.db import get_db
# from src.schemas import ChatHistoryBase, ChatHistoryModel
# from src.repository import chathistory as repository_history
# from src.repository import chats as repository_chats
# from src.services.auth import auth_service
# from src.services.chat_service import chat_service
# from src.conf import messages
# from src.services.role import RoleAccess
# from src.database.models import User, Role, Chat
#
# router = APIRouter(prefix='/start', tags=["chat_service"])
#
# allowed_get_history = RoleAccess([Role.admin, Role.moderator, Role.user])
# allowed_add_messages = RoleAccess([Role.user, Role.admin])
#
#
# @router.post("/{chat_id}", response_model=ChatHistoryModel, status_code=status.HTTP_201_CREATED,
#              dependencies=[Depends(allowed_add_messages)])
# async def ask_question(chat_id: int, body: ChatHistoryBase, db: Session = Depends(get_db),
#                        current_user: User = Depends(auth_service.get_current_user)):
#     # request_body = await request.json()
#     # user_question = request_body.get("user_question", "")
#     #
#     # answer = await chat_service.create_question_and_response_in_history(chat_id, user_question, db, current_user)
#
#     answer = await chat_service.create_question_and_response_in_history(chat_id, db, current_user, body.message)
#
#     return answer
