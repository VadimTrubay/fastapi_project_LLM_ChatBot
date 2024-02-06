import pickle

# import langchain
import streamlit as st
from dotenv import load_dotenv

from pages.src.auth_services import FILE_NAME
from pages.src.chats_history_services import get_chat_list, create_message, get_history, delete_chat

# langchain.verbose = False


def get_chat_history(chat_id):
    """
    The get_chat_history function takes a chat_id as an argument and returns the history of that chat.

    :param chat_id: Get the chat's history
    :return: A list of messages, so we can print them out
    """
    res = get_history(chat_id, access_token)
    if res.status_code == 200:
        st.write("In previous episodes...: ")
        return [item["message"] for item in res.json()]
    else:
        st.write("Chat's history: ")
        return "It's empty"


def delete_chat_history(chat_id):
    """
    The delete_chat_history function deletes the chat history of a given chat.
        Args:
            chat_id (str): The id of the chat to delete.

    :param chat_id: Identify the chat to be deleted
    :return: A response object
    """
    res = delete_chat(chat_id, access_token)
    if res.status_code == 404:
        st.error("Chat not found.")
    else:
        st.warning("Chat deleted successfully.")


# main funk  Streamlit
def main():
    """
    The main function is the entry point for the application.
    It creates a Streamlit app and runs it.

    :return: The access token
    """
    st.title("Exist chats")

    # get list of chats from the server
    chat_list = get_chat_list(access_token)

    # display a list of chats for selection
    selected_chat_index = st.selectbox("Select a chat:", [chat["title_chat"] for chat in chat_list])

    # find the chat_id of the selected chat
    selected_chat_id = None
    for chat in chat_list:
        if chat["title_chat"] == selected_chat_index:
            selected_chat_id = chat["id"]

            if st.button("Delete Chat"):
                if selected_chat_id:
                    delete_chat_history(selected_chat_id)

            if chat["chat_data"]:
                st.write("Chat has context, you can continue")
            else:
                st.write("Reload document, chat lost context")
            st.write(f"Selected chat: {selected_chat_index}")
            exist_history = get_chat_history(chat["id"])
            st.write(exist_history)

    if selected_chat_id is not None:

        # Enter text for a question
        user_question = st.text_input("Ask a question about your documents:")

        # Button to create a question and receive an answer
        if st.button("Send a question"):
            response = create_message(selected_chat_id, user_question, access_token)
            st.write(f"Your question: {user_question}")
            st.write(f"Bot's answer: {response['message']}")


if __name__ == "__main__":
    load_dotenv()
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
