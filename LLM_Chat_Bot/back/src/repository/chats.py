from typing import List
import os
import pathlib

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()
from src.database.models import User, Chat, Role
from src.schemas import ChatBase
from src.services.file_service import delete_source_file, delete_vectorstore, merge_faiss_by_chat_ids, save_text_to_file

root_directory = pathlib.Path(__file__).parent.parent.parent.parent
data_folder = settings.data_folder
raw_data = "raw_data"
FULL_PATH = os.path.join(root_directory, data_folder, raw_data)


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
            await delete_vectorstore(chat_id)

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


async def merge_chats(chats_to_merge: List[int], db: Session, user: User) -> Chat | None:
    """
    The **merge_chats** function merges multiple chats into a new chat.

    :param chats_to_merge: List[int]: List of chat ids to merge
    :param db: Session: Access the database
    :param user: User: Get the current user
    :return: The new chat object representing the merged chats
    """
    # Call merge_faiss_by_chat_ids with the chat_ids to merge
    # await merge_faiss_by_chat_ids(chats_to_merge)

    # Save the merged chat data to a new resource file using the function
    # Copy data from the chats being merged into the new chat
    merged_chat_files = ""
    for chat_id in chats_to_merge:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            with open(chat.file_url, "r", encoding="utf-8") as chat_file:
                chat_data = chat_file.read()
                merged_chat_files += chat_data
    title_chat = f"Merged Chats {', '.join(map(str, chats_to_merge))}"
    chat_file_path = os.path.join(FULL_PATH, f"{title_chat}.txt")
    file_url = await save_text_to_file(merged_chat_files, chat_file_path)

    # Create a new chat that represents the merged chats
    new_chat = Chat(title_chat=title_chat, chat_data=True, user_id=user.id, file_url=file_url)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    # You may want to add logic here to copy data from the chats being merged into the new chat


    # # Delete the original chats that were merged
    # for chat_id in chats_to_merge:
    #     await delete_chat(chat_id, db, user)

    return new_chat
