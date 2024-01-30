import os
import pathlib

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from src.conf.config import settings
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS = OpenAIEmbeddings()
root_directory = pathlib.Path(__file__).parent.parent.parent.parent
data_folder = settings.data_folder
V_DB = "V_DB"
FULL_PATH = os.path.join(root_directory, data_folder, V_DB)


async def delete_source_file(path):
    file_path = path
    os.remove(file_path)


async def save_vectorstore(vectorstore, chat_id):
    vectorstore.save_local(FULL_PATH, index_name=str(chat_id))


async def load_vectorstore(chat_id):
    vectorstore = FAISS.load_local(FULL_PATH, index_name=str(chat_id),
                            embeddings=EMBEDDINGS)
    return vectorstore


async def delete_vectorstore(chat_id):
    vectorstore_file_path_faiss = os.path.join(FULL_PATH, f"{chat_id}.faiss")
    vectorstore_file_path_pkl = os.path.join(FULL_PATH, f"{chat_id}.pkl")
    if os.path.exists(vectorstore_file_path_faiss):
        os.remove(vectorstore_file_path_faiss)
        os.remove(vectorstore_file_path_pkl)


async def merge_faiss_by_chat_ids(chat_ids):
    # Створюємо порожній об'єкт FAISS для злиття
    merged_faiss = FAISS()

    for chat_id in chat_ids:
        # Формуємо шлях до файлу FAISS для поточного чату
        vectorstore_file_path = os.path.join(FULL_PATH, f"{chat_id}.faiss")

        # Завантажуємо FAISS об'єкт з вказаного файлу
        faiss_obj = FAISS.load_local(FULL_PATH, index_name=chat_id, embeddings=EMBEDDINGS)

        # Злиття поточного об'єкта FAISS з іншим
        merged_faiss.merge_from(faiss_obj)

    return merged_faiss


async def save_text_to_file(text, path):
    """
    The save_text_to_file function takes a string and saves it to a file.

    :param text: Pass the text to be written to a file
    :param path: Specify the location where the file should be saved
    :return: The path of the file that was written to
    """
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    return path
