import pickle
from langchain.schema import HumanMessage, AIMessage
import streamlit as st
from langchain.document_loaders import WebBaseLoader
from pages.src.build_new_chat_services import *
from htmlTemplates import css
from pages.src.auth_services import FILE_NAME

load_dotenv()


def main():
    global language

    st.write(css, unsafe_allow_html=True)

    selected_option = st.sidebar.radio("Select an option:", ["GPT-3.5", "Chat"])

    if selected_option == "GPT-3.5":

        close_chat_button = st.button("Close Chat")
        if close_chat_button:
            close_chat()

        choice = st.radio("Select input:", ["VOICE", "TEXT"], horizontal=True)

        if choice == "VOICE":
            selected_lang = st.radio("Select language:", ["українська", "english", "свинособача"], horizontal=True)
            if st.button("Speak..."):
                if selected_lang == "українська":
                    language = "uk-UA"
                elif selected_lang == "english":
                    language = "en-US"
                elif selected_lang == "свинособача":
                    language = "ru-RU"
                text = voice_input(language)
                gpt_chat(text)

        if choice == "TEXT":
            user_input = st.text_input("Ask a question:")
            gpt_chat(user_input)

    elif selected_option == "Chat":
        close_chat_button = st.button("Close Chat")

        if close_chat_button:
            close_chat()

        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        load_history_button = st.sidebar.button("Load Chat History")

        if load_history_button:
            st.session_state.chat_history = load_chat_history("chat_history.json")
            st.success("Chat history loaded successfully.")

            # Display chat history
            if st.session_state.chat_history:
                st.subheader("Chat History")
                for message in st.session_state.chat_history:
                    if isinstance(message, dict) and "type" in message:
                        if message["type"].lower() == "human":
                            st.write(user_template.replace("{{MSG}}", message.get('content', '')),
                                     unsafe_allow_html=True)
                        elif message["type"].lower() == "ai":
                            st.write(bot_template.replace("{{MSG}}", message.get('content', '')),
                                     unsafe_allow_html=True)
                    elif isinstance(message, HumanMessage):
                        st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                    elif isinstance(message, AIMessage):
                        st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        selected_page = st.selectbox("Select a page for Chat", ["Upload PDF file",
                                                                "Upload TXT file",
                                                                "Upload DOCX file",
                                                                "Enter web link",
                                                                "Enter youtube link",
                                                                "Upload Saved file", ])
        try:
            if selected_page == "Enter web link":
                web_link = st.text_input("Enter a web link:")
                file_name = file_name_web(web_link)
                if st.button("Process Web Link"):
                    loader = WebBaseLoader(web_path=web_link)
                    web_doc = loader.load()
                    with st.spinner("Processing"):
                        raw_text = get_web_text(web_doc)
                    try:
                        save_file(raw_text, file_name)
                        st.success("Saved successfully.")
                        chat(raw_text)
                    except Exception as er:
                        st.warning(f"Error: {er}. No file to save.")

            elif selected_page == "Enter youtube link":
                youtube_link = st.text_input("Enter a youtube link:")
                file_name = file_name_youtube(youtube_link)
                if st.button("Process Web Link"):
                    with st.spinner("Processing"):
                        raw_text = get_youtube_text(youtube_link)
                    try:
                        save_file(raw_text, file_name)
                        st.success("Saved successfully.")
                        chat(raw_text)
                    except Exception as er:
                        st.warning(f"Error: {er}. No file to save.")

            elif selected_page == "Upload PDF file":
                pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'",
                                            accept_multiple_files=True)
                file_name = file_name_pdf(pdf_docs)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        try:
                            raw_text = get_pdf_text(pdf_docs)
                            save_file(raw_text, file_name)
                            chat(raw_text)
                            st.success("Saved successfully.")
                        except Exception as er:
                            st.warning(f"Error: {er}. No file to save.")

            elif selected_page == "Upload TXT file":
                txt_doc = st.file_uploader("Upload your TXTs here and click on 'Process'",
                                           accept_multiple_files=True)
                file_name = file_name_txt(txt_doc)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        raw_text = get_txt_text(txt_doc)
                        try:
                            save_file(raw_text, file_name)
                            st.success("Saved successfully.")
                            chat(raw_text)
                        except Exception as er:
                            st.warning(f"Error: {er}. No file to save.")

            elif selected_page == "Upload DOCX file":
                docs_doc = st.file_uploader("Upload your DOCXs here and click on 'Process'",
                                            accept_multiple_files=True)
                file_name = file_name_docx(docs_doc)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        raw_text = get_docx_text(docs_doc)
                        try:
                            save_file(raw_text, file_name)
                            st.success("Saved successfully.")
                            chat(raw_text)
                        except Exception as er:
                            st.warning(f"Error: {er}. No file to save.")

            elif selected_page == "Upload Saved file":
                new_doc = st.file_uploader("Upload your Saved file and click on 'Process'",
                                           accept_multiple_files=True)
                if st.button("Process"):
                    with st.spinner("Processing"):
                        try:
                            raw_text = get_txt_text(new_doc)
                            st.success("Upload successfully.")
                            chat(raw_text)
                        except Exception as er:
                            st.warning(f"Error: {er}. No file to save.")

        except Exception as ex:
            st.error(f"{ex} Error input!")

        choice = st.radio("Select input:", ["VOICE", "TEXT"], horizontal=True)

        if choice == "TEXT":
            user_question = st.text_input("Ask a question about your documents:books:")
            if user_question:
                handle_userinput(user_question)

        if choice == "VOICE":
            selected_lang = st.radio("Select language:", ["українська", "english", "свинособача"], horizontal=True)
            if st.button("Speak..."):
                if selected_lang == "українська":
                    language = "uk-UA"
                elif selected_lang == "english":
                    language = "en-US"
                elif selected_lang == "свинособача":
                    language = "ru-RU"
                text = voice_input(language)
                handle_userinput(text)


if __name__ == '__main__':
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
