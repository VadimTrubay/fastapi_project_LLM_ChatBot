import os
import json
from pathlib import Path
from urllib.parse import urlparse

import requests
from docx import Document
import openai
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from src.conf.config import settings
from pages.src.auth_services import SERVER_URL, FILE_NAME
import streamlit as st
import speech_recognition as sr
from htmlTemplates import css, bot_template, user_template
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain



data_directory = settings.data_folder
root_directory = os.getcwd()
full_path = os.path.join(root_directory, data_directory)

load_dotenv()


# def save_text_to_file(text, path):
#     """
#     The save_text_to_file function takes a string and saves it to a file.
#
#     :param text: Pass the text to be written to a file
#     :param path: Specify the location where the file should be saved
#     :return: The path of the file that was written to
#     """
#     with open(path, 'w', encoding='utf-8') as file:
#         file.write(text)
#     return path
#
#
# def search_duplicate(store_name):
#     """
#     The search_duplicate function takes in a store name as an argument and searches the directory for a file with that
#     store name. If it finds one, it returns True. Otherwise, it returns None.
#
#     :param store_name: Search for a file with the same name as the store
#     :return: True if the file exists, none otherwise
#     :doc-author: Trelent
#     """
#     search_txt = f"{store_name}.txt"
#     if os.path.exists(full_path) and os.path.isdir(full_path):
#         file_list = os.listdir(full_path)
#         if search_txt in file_list:
#             return True
#     return None
#
#
# def set_data_url(store_name, file_url, acc_token):
#     """
#     The set_data_url function takes in the store name, file url, and access token as parameters.
#     It then creates a dictionary with the title_chat key set to the store name and file_url key set to
#     the file url. It then converts this dictionary into JSON format using json.dumps(). The function
#     then sets up headers for authorization and content type (JSON). Finally it returns a POST request
#     to our API server with data being equal to our JSON formatted data.
#
#     :param store_name: Set the title of the chat
#     :param file_url: Send the url of the file to be uploaded
#     :param acc_token: Authenticate the user
#     :return: A response object
#     :doc-author: Trelent
#     """
#     api_url = SERVER_URL + '/api/chats/'
#     data = {
#         "title_chat": f"{store_name}",
#         "file_url": f"{file_url}"
#     }
#     data_json = json.dumps(data)
#
#     headers = {
#         "Authorization": f"Bearer {acc_token}",
#         'Content-Type': 'application/json'
#     }
#
#     return requests.post(api_url, data=data_json, headers=headers)
#
#
# def get_pdf_text(pdf_doc) -> str:
#     """
#     The get_pdf_text function takes a PDF document as input and returns the text of that document.
#     It does this by using the PyPDF2 library to read in each page of the PDF, extract its text, and then concatenate all
#     of those pages into one string.
#
#     :param pdf_doc: Specify the file path of the pdf document that you want to extract text from
#     :return: A string of text from the pdf document
#     """
#     text = ""
#     pdf_reader = PdfReader(pdf_doc)
#     for page in pdf_reader.pages:
#         text += page.extract_text()
#     return text
#

def gpt_chat(text=None):
    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []
    if text:
        user_input = text
        gpt_response = make_gpt_request(user_input)
        try:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "gpt", "content": gpt_response})
        except Exception as e:
            st.error(f"Error appending to chat_history: {e}")
        try:
            for message in reversed(st.session_state.chat_history):
                role, content = message["role"], message["content"]
                if role == "gpt":
                    st.write(bot_template.replace("{{MSG}}", content), unsafe_allow_html=True)
                elif role == "user":
                    st.write(user_template.replace("{{MSG}}", content), unsafe_allow_html=True)
        except TypeError:
            st.error('object is not subscriptable')


def make_gpt_request(question):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    prompt = "You are chatting with a friendly and helpful friend. Feel free to ask me anything!"

    try:
        completion = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.9,
        )
        text = completion.choices[0].message.content
        return text
    except Exception as er:
        print(er)


def save_file(raw_text, file_name):
    with open(f"history/{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(raw_text)


def voice_input(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            st.write("Listen...")
            audio = r.listen(source)
            text = r.recognize_google(audio, language=lang)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, i didn't get you!")
        # print("I don't understand audio")
        except sr.RequestError as er:
            st.error("Sorry, request was failed!")
            print(f"Could not request results from Speech2Text service; {er}")


def file_name_web(link_doc):
    parsed_url = urlparse(link_doc)
    name = os.path.basename(parsed_url.path)
    file_name, file_extension = os.path.splitext(name)
    return file_name


def get_web_text(web_doc):
    text = ""
    for doc in web_doc:
        text += doc.page_content
    return text


def file_name_youtube(youtube_link):
    file_name = "watch_" + youtube_link.split('watch?v=')[-1]
    return file_name


def get_youtube_text(youtube_link):
    video_id = youtube_link.split('watch?v=')[-1]

    target_language = None
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        target_language = transcript.language_code
        try:
            transcript_data = transcript.fetch()
            translated_transcript = transcript.translate(target_language).fetch()
        except Exception as e:
            print(f"Error fetching transcript: {e}")

    target_language = target_language

    try:
        transcript = transcript_list.find_transcript([target_language])
        transcript_data = transcript.fetch()
        text = " ".join(entry['text'] for entry in transcript_data)
        print(text)
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")


def file_name_pdf(pdf_docs):
    first_doc = pdf_docs[0] if len(pdf_docs) > 0 else None
    if first_doc:
        name = first_doc.name
        file_name, file_extension = os.path.splitext(name)
        return file_name
    return None


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def file_name_docx(docs_doc):
    first_doc = docs_doc[0] if len(docs_doc) > 0 else None
    if first_doc:
        name = first_doc.name
        file_name, file_extension = os.path.splitext(name)
        return file_name
    return None


def get_docx_text(docs_doc):
    text = ""
    try:
        for docx in docs_doc:
            doc = Document(docx)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
    except Exception as e:
        # Handle specific exceptions here, e.g., catching an incomplete file
        st.warning(f"Error reading DOCX file: {e}. No file to save.")
        return None  # Return None to indicate an error

    return text


def file_name_txt(txt_docs):
    first_doc = txt_docs[0] if len(txt_docs) > 0 else None
    if first_doc:
        name = first_doc.name
        file_name, file_extension = os.path.splitext(name)
        return file_name
    return None


def get_txt_text(txt_doc):
    text = ""
    for txt_doc in txt_doc:
        text += txt_doc.getvalue().decode('utf-8') + "\n"
    return text


def chat(raw_text):
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    st.session_state.conversation = get_conversation_chain(vectorstore)


def get_load_text(file_name):
    if file_name is not None:
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            st.warning(f"Error loading file: {e}")
    else:
        st.warning("No file selected.")
        return ""


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']
        chat_history_reversed = st.session_state.chat_history[::-1]

        for i, message in enumerate(chat_history_reversed):
            if i % 2 == 1:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        pass


"""Added history svae/load"""


def save_chat_history(chat_history, file_path):
    def convert_to_dict(obj):
        if isinstance(obj, HumanMessage) or isinstance(obj, AIMessage):
            return obj.__dict__
        return obj

    with open(file_path, "w") as file:
        json.dump(chat_history, file, default=convert_to_dict, indent=2)


def load_chat_history(file_name):
    chat_history_file = Path(file_name)
    if chat_history_file.is_file():
        with open(chat_history_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

            # Manually convert each element to the appropriate type
            chat_history = []
            for item in json_data:
                if 'type' in item:
                    if item['type'].lower() == 'human':
                        chat_history.append(HumanMessage(**item))
                    elif item['type'].lower() == 'ai':
                        chat_history.append(AIMessage(**item))
                else:
                    # Handle other cases as needed
                    chat_history.append(item)

            return reversed(chat_history)
    else:
        return []


def close_chat():
    if st.session_state.conversation is not None:
        chat_history = st.session_state.chat_history
        save_chat_history(chat_history, "chat_history.json")

        st.session_state.conversation = None
        st.session_state.chat_history = None
        st.success("Chat closed.")
        st.rerun()
    else:
        st.warning("No active chat to close.")




