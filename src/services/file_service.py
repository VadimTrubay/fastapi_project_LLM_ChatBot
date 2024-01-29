# import pickle
import os
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
# from langchain.vectorstores import FAISS

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from dotenv import load_dotenv

load_dotenv()

supported_files = ['pdf', 'csv', 'doc', 'docx', 'enex', 'eml', 'epub', 'html', 'md', 'odt', 'ppt', 'pptx', 'txt']

LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (UnstructuredEmailLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}



async def before_chat_insert(file_content):
    with open(file_content, "r", encoding="utf-8") as file:
        text = file.read()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # embeddings = OpenAIEmbeddings()
    # # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    #
    # vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    # # vectorstore = Bagel.from_texts(cluster_name="testing", texts=text_chunks, embedding=embeddings)
    # context = pickle.dumps(vectorstore)

    return chunks
    # return context

async def delete_source_file(path):
    file_path = path
    os.remove(file_path)