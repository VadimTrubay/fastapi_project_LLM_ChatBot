from sqlalchemy.orm import Session
from sqlalchemy import and_
import ast


from src.database.models import User, ChatHistory
from src.schemas import ChatHistoryBase
from src.services.chat_service import get_context, get_conversation_chain


async def create_message(chat_id: int, body: ChatHistoryBase, db: Session, user: User) -> ChatHistory:
    """
    The **create_message** function adds a new history to the database.

    :param db: Session: Access the database
    :param user: User: Get the user_id from the logged-in user
    :param chat: Chat: Get the chat_id
    :return: A new chat_history object
    """
    context = await get_context(chat_id, db, user)
    answer = get_conversation_chain(body.message, context)

    response_dict = ast.literal_eval(answer)
    user_question = 'Q: ' + response_dict['user_messages'][0]
    bot_response = 'A: '+ response_dict['bot_messages'][0]

    question = ChatHistory(message=user_question, user_id=user.id, chat_id=chat_id)
    response = ChatHistory(message=bot_response, user_id=user.id, chat_id=chat_id)
    # new_chat_history = ChatHistory(message=body.message, user_id=user.id, chat_id=chat_id)
    db.add(question)
    db.add(response)

    db.commit()
    db.refresh(response)
    return response


async def get_history_by_chat(chat_id: int, db: Session) -> ChatHistory:
    """
    The **get_history_by_chat** function returns a history from the database by chat_id and user.

    :param chat_id: int: Specify the id of the chat that we want to retrieve
    :param db: Session: Access the database
    # :param user: User: Check if the user is authorized to see chat
    :return: The messages with the given id, if it exists
    """
    return db.query(ChatHistory).filter(and_(ChatHistory.chat_id == chat_id)). \
        order_by(ChatHistory.created_at).all()
