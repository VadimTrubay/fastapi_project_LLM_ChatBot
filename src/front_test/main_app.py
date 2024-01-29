import json
from pathlib import Path
import os
import streamlit as st
import requests
# import subprocess
import openai
from langchain.document_loaders import WebBaseLoader
from htmlTemplates import css

from chat_functions import *

# Base URL for the FastAPI application
BASE_URL = "http://localhost:8000/api/auth"
#BASE_URL = "http://134.122.104.117:8000/api/auth"
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

BASE_DIR = Path(__file__).resolve().parent.parent
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# print(f"!!!!!!!!!!{OPENAI_API_KEY=}")


class State:
    current_page = "Sign Up"
    redirect_to_login = False
    redirect_to_main = False
    user_info = False


def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    api_key = st.text_input("ApiKey")

    if st.button("Sign Up"):
        if password == confirm_password:
            data = {
                "username": username,
                "email": email,
                "password": password,
                "api_key": api_key
            }
            response = requests.post(f"{BASE_URL}/signup", json=data)
            st.write("Response Status Code:", response.status_code)
            # st.write("Response Content:", response.content.decode("utf-8"))
            try:
                # response_json = response.json()
                # st.write("Response JSON:", response_json)  # Print the entire JSON response for debugging
                message = response.status_code

                if message == 201:
                    st.success("Sign up successful! Please confirm your email and you may proceed with login!")
                    # Set the redirect flag to True
                    # state.redirect_to_login = True

                else:
                    st.error("No message found in the response.")
            except KeyError:
                st.error("Unexpected response format. Please check the server response.")
        else:
            st.error("Passwords do not match.")

        # Check if redirection is required
        # if getattr(state, 'redirect_to_login', False):
        #     # Reset the redirect flag
        #     state.redirect_to_login = True
        #     # Redirect to the login page
        #     state.current_page = "Log In"


# Function to log in a user
def login():
    state = State()
    st.title("Log In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        data = {
            "username": email,
            "password": password
        }
        response = requests.post(f"{BASE_URL}/login", data=data)
        if response.status_code == 200:
            st.success("Log In Successful")
            state.user_info = True
            print(f"state.user_info: !!! IS {state.user_info}")
            # state.redirect_to_main = True
            # state.user_info = response.json().get("user_info")
            # st.json(response.json())
            # st.session_state.runpage = main_page
            return True

        else:
            st.error("Log In Failed")
            st.text(response.text)
            print(f"{state.user_info=}")
            return False

        # if getattr(state, 'redirect_to_main', False):
        #     # Reset the redirect flag
        #     state.redirect_to_main = False
        #     # Redirect to the main page
        #     st.experimental_set_query_params(page="Main Page")


def main_page(state):
    st.title("Main Page")
    # Check if the user is logged in
    if state.user_info:
        st.write("Welcome to the main page!")
        st.button("Log Out", on_click=lambda: state.__setattr__("user_info", False))
    else:
        st.write("Please log in to access the main page.")
        st.button("Log In", on_click=lambda: state.__setattr__("current_page", "Log In"))


# Function to refresh the access token
def refresh_token():
    st.title("Refresh Token")
    refresh_token = st.text_input("Refresh Token")

    if st.button("Refresh Token"):
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = requests.get(f"{BASE_URL}/refresh_token", headers=headers)
        if response.status_code == 200:
            st.success("Token Refreshed Successfully")
            st.json(response.json())
        else:
            st.error("Token Refresh Failed")
            st.text(response.text)


# Function to confirm email
def confirmed_email():
    st.title("Confirm Email")
    token = st.text_input("Confirmation Token")

    if st.button("Confirm Email"):
        response = requests.get(f"{BASE_URL}/confirmed_email/{token}")
        st.json(response.json())


# Function to request email confirmation
def request_email():
    st.title("Request Email Confirmation")
    email = st.text_input("Email")

    if st.button("Request Email Confirmation"):
        data = {"email": email}
        response = requests.post(f"{BASE_URL}/request_email", json=data)
        st.json(response.json())


# Function to reset password
# def reset_password(email: str):
#     st.title("Reset Password")
#     # email = st.text_input("Email")
#     email = email
#
#     if st.button("Reset Password"):
#         data = {"email": email}
#         response = requests.post(f"{BASE_URL}/reset_password", json=data)
#         st.json(response.json())
#
#         reset_password_token = response.json().get("reset_password_token")
#
#         return reset_password_token
#
#
# # Function to confirm password reset
# def password_reset_confirm():
#     st.title("Password Reset Confirmation")
#     email = st.text_input("Email")
#     token = reset_password(email)
#
#
#     if st.button("Confirm Password Reset"):
#         response = requests.get(f"{BASE_URL}/password_reset_confirm/{token}")
#         st.json(response.json())
#         result = response.json().get("token")
#         print(result)
#         return result
#
# # Function to update password
# def update_password():
#     st.title("Update Password")
#     reset_password_token = password_reset_confirm()
#     print(reset_password_token, type(reset_password_token))
#     new_password = st.text_input("New Password", type="password")
#     confirm_password = st.text_input("Confirm Password", type="password")
#
#     if st.button("Update Password"):
#         if new_password == confirm_password:
#             data = {
#                 "reset_password_token": reset_password_token,
#                 "new_password": new_password,
#                 "confirm_password": confirm_password
#             }
#             response = requests.post(f"{BASE_URL}/set_new_password", json=data)
#             st.json(response.json())
#         else:
#             st.error("Passwords do not match.")


# def reset_password(email):
#     data = {"email": email}
#     response = requests.post(f"{BASE_URL}/reset_password", json=data)
#     print(f"{response.json()}")
#     print(f'Message is: {response.json().get("message")}')


def reset_password(email):
    data = {"email": email}

    try:
        response = requests.post(f"{BASE_URL}/get_new_token", json=data)
        print(response.json())
        if response.status_code == 200:
            token = response.json().get("token")
            # print(f"TOKEN IS :::::: NOW::: ::: is: !!! {token=}")
            return token
        else:
            print(f"Failed to initiate password reset. Response: {response}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def password_reset_confirm(token):
    print(f"TOKEN:::{token}")
    response = requests.get(f"{BASE_URL}/password_reset_confirm/{token}")
    # answer = requests.post(f"{BASE_URL}/password_reset_confirm/{token}")
    # st.write(f"Password Reset Confirmation Response: {response.json().get('token')}")
    # st.write(f"Password Reset Confirmation Answer: {answer.json().get('token')}")
    print(f"Password Reset Confirmation Response: {response.json().get('token')}")
    # print((f"Password Reset Confirmation Answer: {answer.json().get('token')}"))
    # return response.json().get("token")
    return response.json().get("token")


def update_password(reset_password_token, new_password, confirm_password):
    st.title("Update Password")
    if new_password == confirm_password:
        data = {
            "reset_password_token": reset_password_token,
            "new_password": new_password,
            "confirm_password": confirm_password
        }
        response = requests.post(f"{BASE_URL}/set_new_password", json=data)
        st.json(response.json())
        return response.json()

def gpt_chat(text=None):
    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        # or st.session_state.chat_history is None
        st.session_state.chat_history = []

    if text:
        user_input = text
        gpt_response = make_gpt_request(user_input)
        try:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "gpt", "content": gpt_response})
            # chat_history_reversed = st.session_state.chat_history[::-1]
        except Exception as e:
            st.error(f"Error appending to chat_history: {e}")
        try:
            for message in reversed(st.session_state.chat_history):
                role, content = message["role"], message["content"]
                if role == "gpt":
                    st.write(bot_template.replace("{{MSG}}", content), unsafe_allow_html=True)
                elif role == "user":
                    st.write(user_template.replace("{{MSG}}", content), unsafe_allow_html=True)
        # try:
        #     for i, message in enumerate(chat_history_reversed):
        #         if i % 2 == 0:
        #             st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        #         else:
        #             st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        except TypeError:
            st.error('object is not subscriptable')


# def gpt_chat(text=None):
#     # st.title("GPT Chat")
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#
#     if text:
#         user_input = text
#         gpt_response = make_gpt_request(user_input)
#         st.session_state.chat_history.append({"role": "gpt", "content": gpt_response})
#         chat_history_reversed = st.session_state.chat_history[::-1]
#         try:
#             for i, message in enumerate(chat_history_reversed):
#                 if i % 2 == 0:
#                     st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
#                 else:
#                     st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
#         except TypeError:
#             st.error('object is not subscriptable')


def make_gpt_request(question):
    openai.api_key = OPENAI_API_KEY
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


def main():
    global lan
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")

    state = State()
    selected_page = None
    # user_info = None
    st.title("FastAPI Streamlit App")
    st.write(css, unsafe_allow_html=True)

    selected_option = st.sidebar.radio("Select an option:", ["Auth", "Chat", "GPT-3.5"])

    # Based on the selected option, display different page choices
    if selected_option == "Auth":
        # print(state.user_info)
        selected_page = st.sidebar.selectbox("Select a page", ["Sign Up", "Log In", "Refresh Token",
                                                               "Confirm Email", "Request Email Confirmation",
                                                               "Reset Password", "Password Reset Confirmation",
                                                               "Update Password"])

    elif selected_option == "GPT-3.5":
        if not state.user_info:
            st.success("Login success")
        choice = st.sidebar.radio("Select input:", ["VOICE",
                                                    "TEXT"
                                                    ])
        if choice == "TEXT":
            user_input = st.sidebar.text_input("Ask a question:")
            gpt_chat(user_input)

        if choice == "VOICE":
            selected_lang = st.sidebar.radio("Select language:", ["українська",
                                                                  "english",
                                                                  "свинособача"
                                                                  ])

            if selected_lang == "українська":
                lan = "uk-UA"
            elif selected_lang == "english":
                lan = "en-US"
            elif selected_lang == "свинособача":
                lan = "ru-RU"

            if st.sidebar.button("Speak..."):
                text = voice_input(lan)
                gpt_chat(text)

    elif selected_option == "Chat":
        close_chat_button = st.button("Close Chat")


        if close_chat_button:
            close_chat()
        if not state.user_info:
            st.success("Login success")

            if "conversation" not in st.session_state:
                st.session_state.conversation = None
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = None

            load_history_button = st.button("Load Chat History")

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

                # # Display chat history
                # if st.session_state.chat_history:
                #     st.subheader("Chat History")
                #     for message in st.session_state.chat_history:
                #         if isinstance(message, dict) and "type" in message:
                #             if message["type"].lower() == "human":
                #                 st.text(f"User: {message['content']}")
                #             elif message["type"].lower() == "ai":
                #                 st.text(f"AI: {message['content']}")
                #         elif isinstance(message, HumanMessage):
                #             st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
                #         elif isinstance(message, AIMessage):
                #             st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
                #




            choice = st.sidebar.radio("Select input:", ["VOICE",
                                                        "TEXT"
                                                        ])
            if choice == "TEXT":
                user_question = st.sidebar.text_input("Ask a question about your documents:books:")
                if user_question:
                    handle_userinput(user_question)
            if choice == "VOICE":
                selected_lang = st.sidebar.radio("Select language:", ["українська",
                                                                      "english",
                                                                      "свинособача"
                                                                      ])

                if selected_lang == "українська":
                    lan = "uk-UA"
                elif selected_lang == "english":
                    lan = "en-US"
                elif selected_lang == "свинособача":
                    lan = "ru-RU"

                if st.sidebar.button("Speak..."):
                    text = voice_input(lan)
                    handle_userinput(text)


            selected_page = st.sidebar.selectbox("Select a page for Chat", ["Upload PDF file",
                                                                            "Upload TXT file",
                                                                            "Upload DOCX file",
                                                                            "Enter web link",
                                                                            "Enter youtube link",
                                                                            "Upload Saved file", ])

            with st.sidebar:
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

        else:
            st.warning("Please log in to access the chat.")
            selected_page = "Log In"

    if selected_page == "Sign Up":
        signup()
    elif selected_page == "Log In":
        state.user_info = login()
        # st.success("Login successfully")

    elif selected_page == "Request Email Confirmation":
        request_email()

    elif selected_page == "Password Reset Confirmation":
        st.title("Password Reset Flow")

        # Step 1: Reset Password
        email_for_reset = st.text_input("Enter your email for password reset:")
        reset_token = reset_password(email_for_reset)
        # st.write(f"Reset Password Token: {reset_token}")
        # if reset_token:
        #     st.success("Password reset initiated. ")
        #     st.write(f"Reset Password Token: {reset_token}")
        # else:
        #     st.error("Failed to initiate password reset.")

        # if st.button("Reset Password"):
        #     # reset_token = reset_password(email_for_reset)
        #     st.success("Password reset initiated. Check your email for instructions.")

        # Step 2: Confirm Password Reset
        if reset_token:
            st.success("Password reset initiated. ")
            st.write(f"Reset Password Token: {reset_token}")
            password_reset_confirm(reset_token)
            new_password = st.text_input("Enter your new password:", type="password")
            print(f"!!!!!!! !!!!First Pas {new_password}")
            confirm_password = st.text_input("Confirm your new password:")
            print(f"!!!!!!! !!!!!Second Pas {confirm_password}")
            # if st.button("Confirm Password Reset"):
            #     st.success("Password reset confirmed.")

            # Step 3: Update Password
            # confirmed_token = password_reset_confirm(email_for_reset, token_for_confirmation)
            # new_password = st.text_input("Enter your new password:", type="password")
            # print(f"!!!!!!! !!!!First Pas {new_password}")
            # confirm_password = st.text_input("Confirm your new password:")
            # print(f"!!!!!!! !!!!!Second Pas {confirm_password}")
            if st.button("Update Password"):
                # if new_password == confirm_password:
                # Use the confirmed_token from the confirmation step
                # confirmed_token = password_reset_confirm(email_for_reset, token_for_confirmation)
                update_password(reset_token, new_password, confirm_password)
                st.success("Password updated successfully.")


if __name__ == "__main__":
    main()
