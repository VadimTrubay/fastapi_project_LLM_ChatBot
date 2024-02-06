import json
import pickle
import configparser

import requests

config = configparser.ConfigParser()
config.read("config.ini")

FILE_NAME = config.get("DEV", "token_name")
SERVER_URL = config.get("DEV", "app_url")


def load_token(filename=FILE_NAME):
    """
    The load_token function is used to load the token from a file.
        If the file does not exist, it will create one with an empty token and refresh_token.
        The function returns a tuple of (access_token, refresh_token)

    :param filename: Specify the name of the file that is being opened
    :return: A tuple of the access token and refresh token
    :doc-author: Trelent
    """
    try:
        with open(FILE_NAME, "rb") as fh:
            result = pickle.load(fh)
        # result = get_refresh_token(result[1])
        return result
    except IOError:
        with open(FILE_NAME, "wb") as fh:
            pickle.dump((None, None), fh)


def save_token(acc_token, ref_token):
    """
    The save_token function saves the access and refresh tokens to a file.
        The function takes two arguments: acc_token and ref_token.
        It then opens the FILE_NAME file in write binary mode, dumps the tokens into it,
        and closes it.

    :param acc_token: Store the access token and the ref_token parameter is used to store the refresh token
    :param ref_token: Store the refresh token in a file
    :return: A tuple of the access token and refresh token
    :doc-author: Trelent
    """
    with open(FILE_NAME, "wb") as fh:
        pickle.dump((acc_token, ref_token), fh)


def login(username, password):
    """
    The login function takes in a username and password, and returns an access token if the login is successful.
    If the login fails, it will return None. If the user has not confirmed their email address yet, it will return
    &quot;Email not confirmed&quot;. The function uses requests to send a POST request to /api/auth/login with data containing
    the username and password.

    :param username: Pass the username to the login function
    :param password: Send the password to the server
    :return: A tuple of access and refresh tokens
    :doc-author: Trelent
    """
    data = {"username": username, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/login", data=data)
    if response.status_code == 200:
        return response.json()["access_token"], response.json()["refresh_token"]
    elif response.json().get("detail") == "Email not confirmed":
        return "Email not confirmed"
    else:
        return None


def signup(username, email, password):
    """
    The signup function takes in a username, email, and password.
    It then sends a POST request to the server with those parameters as JSON data.
    The response is returned as JSON.

    :param username: Create a username for the user
    :param email: Store the email of the user
    :param password: Set the password of the user
    :return: A json object with the following keys:
    :doc-author: Trelent
    """
    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/signup", data=json.dumps(data))
    return response.json()


def get_user_info(acc_token, ref_token):
    """
    The get_user_info function takes in an access token and a refresh token,
    and returns the user's information. If the access token is expired, it will
    use the refresh token to get a new one.

    :param acc_token: Authenticate the user
    :param ref_token: Get a new access token if the current one is expired
    :return: The user information
    :doc-author: Trelent
    """
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        return response.json()
    acc_token, ref_token = get_refresh_token(ref_token)
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        save_token(acc_token, ref_token)
        return response.json()
    return None, None


def get_refresh_token(ref_token):
    """
    The get_refresh_token function takes in a refresh token and returns an access token.
        It does this by sending the refresh token to the server, which then sends back a new access_token and
        refresh_token. The function returns both of these tokens.

    :param ref_token: Get the access token and refresh token
    :return: A tuple of the access token and refresh token
    :doc-author: Trelent
    """
    headers = {"Authorization": f"Bearer {ref_token}"}
    response = requests.get(f"{SERVER_URL}/api/auth/refresh_token", headers=headers)
    if response.json().get("access_token"):
        return response.json()["access_token"], response.json()["refresh_token"]
    return None, None


def set_new_pass(pass_token, password, password_confirm):
    """
    The set_new_pass function takes in a password reset token, a new password, and the confirmation of that new
    password. It then sends those values to the server as JSON data. If it receives an HTTP 200 response from the server,
    it returns that response; otherwise it returns whatever error message was received.

    :param pass_token: Identify the user
    :param password: Set the new password
    :param password_confirm: Confirm the password
    :return: A response object
    :doc-author: Trelent
    """
    data = {"reset_password_token": pass_token, "new_password": password, "confirm_password": password_confirm}
    response = requests.post(f"{SERVER_URL}/api/auth/set_new_password", data=json.dumps(data))
    if response.status_code == 200:
        return response
    return response


def request_email(email_):
    """
    The request_email function takes in an email address as a string and sends a request to the server
    to send an email with a link to reset the password. The function returns True if successful, False otherwise.

    :param email_: Send a request to the server for an email
    :return: A dictionary with a key &quot;success&quot; and a value of true or false
    :doc-author: Trelent
    """
    data = {"email": email_}
    response = requests.post(f"{SERVER_URL}/api/auth/request_email", data=json.dumps(data))
    print(response.json())
    return response.json()


def reset_password(email):

    """
    The reset_password function takes in an email address and sends a password reset link to that email.
        The function returns the response from the server, which is a JSON object
    :param email: Identify the user
    :return: A json object with the key &quot;message&quot; and value &quot;email sent&quot;
    :doc-author: Trelent
    """
    data = {"email": email}
    response = requests.post(f"{SERVER_URL}/api/auth/reset_password", data=json.dumps(data))
    print(response.json())
    return response.json()


def set_avatar(acc_token, data):

    """
    The set_avatar function takes in an access token and a file object.
    It then sends a PATCH request to the server with the access token as an authorization header,
    and the file object as data. The function returns a JSON response from the server.

    :param acc_token: Authenticate the user
    :param data: Pass the image data to the server
    :return: The user's information
    :doc-author: Trelent
    """
    headers = {"Authorization": f"Bearer {acc_token}"}
    files = {'file': data}
    response = requests.patch(f"{SERVER_URL}/api/users/avatar", files=files, headers=headers)
    return response.json()
