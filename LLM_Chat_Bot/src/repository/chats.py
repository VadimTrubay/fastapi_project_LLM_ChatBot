from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from src.database.models import User, Chat, Role
from src.schemas import ChatBase
from src.services.file_service import delete_source_file


async def create_chat(body: ChatBase, db: Session, user: User) -> Chat:
    """
    The **create_chat** function adds a new chat to the database.

    :param body: ChatBase: Get the title_chat and file_url from the request body
    :param db: Session: Access the database
    :param user: User: Get the user_id from the logged-in user
    :return: A chat object
    """
    context = True

    new_chat = Chat(title_chat=body.title_chat, chat_data=context, file_url=body.file_url, user_id=user.id)
    # new_chat = Chat(title_chat=body.title_chat, file_url=body.file_url, user_id=user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


async def delete_chat(chat_id: int, db: Session, user: User) -> Chat | None:
    """
    The **delete_chat** function deletes a chat from the database. The chat can be deleted by Admin and Moderator #my own chat????

    :param chat_id: int: Identify the chat to be deleted
    :param db: Session: Connect to the database
    :param user: User: Check if the user is Admin or Moderator and authorized to delete a chat
    :return: The chat that was deleted
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        if user.roles in [Role.admin, Role.moderator] or chat.user_id == user.id:
            await delete_source_file(chat.file_url)
            db.delete(chat)
            db.commit()
    return chat


async def get_chat_by_id(chat_id: int, db: Session, user: User) -> Chat | None:
    """
    The **get_chat_by_id** function returns a chat from the database by chat_id.

    :param chat_id: int: Specify the id of the chat that we want to retrieve
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to see chat
    :return: The chat with the given id, if it exists
    """
    return db.query(Chat).filter(and_(Chat.id == chat_id, Chat.user_id == user.id)).first()


async def get_chats(limit: int, offset: int, user: User, db: Session) -> list | None:
    """
    The **get_chats** function gets all the chats from the database.

    :param limit: int: The number of images to return
    :param offset: int: The number of images to skip
    :param user: User: The user object
    :param db: Session: A connection to our Postgres SQL database.
    :return: A list of chats objects
    """
    chats = db.query(Chat).filter(and_(Chat.user_id == user.id)). \
        order_by(desc(Chat.created_at)).limit(limit).offset(offset).all()
    return chats
