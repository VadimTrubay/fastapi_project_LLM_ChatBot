import os
import json
from pathlib import Path
from urllib.parse import urlparse
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from langchain.schema import HumanMessage, AIMessage
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from youtube_transcript_api import YouTubeTranscriptApi

from htmlTemplates import css, bot_template, user_template
import speech_recognition as sr


# from src.config.config import settings

# OPENAI_API_KEY = "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"
load_dotenv()


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


# def save_chat_history(chat_history, file_name):
#     print("Chat History:", chat_history)
#     chat_history_file = Path(file_name)
#     with open(chat_history_file, 'w', encoding='utf-8') as file:
#         json.dump(chat_history, file)

def save_chat_history(chat_history, file_path):
    def convert_to_dict(obj):
        if isinstance(obj, HumanMessage) or isinstance(obj, AIMessage):
            return obj.__dict__
        return obj

    with open(file_path, "w") as file:
        json.dump(chat_history, file, default=convert_to_dict, indent=2)


# def load_chat_history(file_name = "chat_history.json"):
#     chat_history_file = Path(file_name)
#     if chat_history_file.is_file():
#         with open(chat_history_file, 'r', encoding='utf-8') as file:
#             # Use object_hook to convert dictionaries to custom classes
#             return json.load(file, object_hook=convert_to_object)
#     else:
#         return []
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

            return chat_history
    else:
        return []



# def convert_to_object(obj_dict):
#     if isinstance(obj_dict, dict):
#         if 'content' in obj_dict and 'type' in obj_dict:
#             if obj_dict['type'].lower() == 'human':
#                 return HumanMessage(**obj_dict)
#             elif obj_dict['type'].lower() == 'ai':
#                 return AIMessage(**obj_dict)
#     return obj_dict


# def convert_to_object(obj_dict):
#     if 'content' in obj_dict and 'type' in obj_dict:
#         if obj_dict['type'].lower() == 'human':
#             return HumanMessage(**obj_dict)
#         elif obj_dict['type'].lower() == 'ai':
#             return AIMessage(**obj_dict)
#     return obj_dict

# def load_chat_history(file_name):
#     chat_history_file = Path(file_name)
#     if chat_history_file.is_file():
#         with open(chat_history_file, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     else:
#         return []

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


# def close_chat():
#     if st.session_state.conversation is not None:
#         st.session_state.conversation = None
#         st.session_state.chat_history = None
#         st.success("Chat closed.")
#         st.rerun()
#     else:
#         st.warning("No active chat to close.")
