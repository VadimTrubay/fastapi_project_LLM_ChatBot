import os
import pathlib

from fastapi import HTTPException, status
from typing import List
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import Replicate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sqlalchemy.orm import Session

from src.conf import messages
from src.database.models import User
from src.repository.chats import get_chat_by_id
from src.conf.config import settings
from src.services.file_service import load_vectorstore, save_vectorstore
from dotenv import load_dotenv
load_dotenv()
root_directory = pathlib.Path(__file__).parent.parent.parent.parent
data_folder = settings.data_folder
V_DB = "V_DB"
FULL_PATH = os.path.join(root_directory, data_folder, V_DB)
EMBEDDINGS = OpenAIEmbeddings()
# EMBEDDINGS = HuggingFaceEmbeddings()


async def get_context(chat_id: int, db: Session, user: User) -> List:
    """
    The get_context function takes a chat_id, db, and user as parameters.
    It then calls the get_chat_by_id function to retrieve the chat with that id from the database.
    Then it creates an instance of CharacterTextSplitter class which splits text into chunks based on character count

    :param chat_id: int: Identify the chat that we want to get the context from
    :param db: Session: Access the database
    :param user: User: Get the user's id
    :return: A list of strings, each string containing 1000 characters with overlap 200 characters
    """
    chat = await get_chat_by_id(chat_id, db, user)
    context = chat.file_url
    if context is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    with open(context, "r", encoding="utf-8") as file:
        text = file.read()

    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '(', '?', '=', '>', '.', ')', '!', ' ', ''],
        # separator="\n",
        chunk_size=1024,
        chunk_overlap=64,
        length_function=len,
    )
    # chunks = text_splitter.split_text(text)
    chunks = text_splitter.split_text(text)

    return chunks



async def get_conversation_chain(user_question, context, chat_id) -> str:
    """
    The get_conversation_chain function takes in a user question and context,
    and returns the conversation chain between the user and bot.

    :param user_question: Store the user's question
    :param context: Create a vectorstore that is used to retrieve the closest context
    :return: A string that contains the user's question and the bot's response
    """
    vectorstore_file_path = os.path.join(FULL_PATH, f"{chat_id}.faiss")
    if os.path.exists(vectorstore_file_path):
        vectorstore = await load_vectorstore(chat_id)
    else:
        vectorstore = FAISS.from_texts(texts=context, embedding=EMBEDDINGS)
        await save_vectorstore(vectorstore, chat_id)

    llm = ChatOpenAI(model='gpt-3.5-turbo')
    # Initialize Replicate Llama2 Model
    # llm = Replicate(
    #     model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
    #     input={"temperature": 0.75, "max_length": 3000}
    # )

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )

    response = conversation_chain({'question': user_question})
    chat_history = response['chat_history']

    # for separate question/answer items
    response_dict = {'user_messages': [], 'bot_messages': []}

    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            response_dict['user_messages'].append(message.content)
        else:
            response_dict['bot_messages'].append(message.content)

    return str(response_dict)
