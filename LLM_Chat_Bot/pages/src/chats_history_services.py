import requests

from pages.src.auth_services import SERVER_URL, FILE_NAME


def get_chat_list(access_token):
    """
    The get_chat_list function returns a list of all the chats that the user is currently in.
    The function makes a GET request to /api/chats, which returns an array of chat objects.
    Each chat object contains information about the chat, including its id and name.

    :return: A list of chats
    """
    api_url = SERVER_URL + "/api/chats"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def create_message(chat_id, message, acc_token):
    """
    The create_message function takes in a chat_id, message, and acc_token.
    It then uses the SERVER_URL to create an api url for the specific chat id.
    The function then creates headers with authorization and content type as json.
    The data is set to a dictionary of message:message (the user's input).  The response is created using requests
    post method with the api url, data, and headers as parameters.
    If status code 201 is returned from server it returns response in json format otherwise
     it returns error creating question.

    :param chat_id: Specify which chat the message should be sent to
    :param message: Send a message to the chat
    :param acc_token: Authenticate the user
    :return: The message id
    :doc-author: Trelent
    """
    api_url = SERVER_URL + f"/api/history/{chat_id}"
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    data = {"message": message}
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return "Error creating question"


def get_history(chat_id, acc_token):
    """
    The get_history function takes in a chat_id and an access token,
    then makes a GET request to the server's /api/history/&lt;chat_id&gt; endpoint.
    The response is returned as JSON.

    :param chat_id: Identify the chat that we want to retrieve the history from
    :param acc_token: Authenticate the user
    :return: A list of messages
    :doc-author: Trelent
    """
    api_url = SERVER_URL + f"/api/history/{chat_id}"
    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    return response


def delete_chat(chat_id, access_token):
    """
    The delete_chat function takes in a chat_id and deletes the chat from the database.
        It returns an error message if the chat is not found, or a success message if it is.

    :param chat_id: Specify which chat to delete
    :return: A response object
    """
    api_url = SERVER_URL + f"/api/chats/{chat_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(api_url, headers=headers)
    return response
