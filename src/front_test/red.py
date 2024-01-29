import streamlit as st

# Create a variable to store the user login state
is_user_logged_in = False

# Placeholder for dynamic content
content_placeholder = st.empty()

# Login page
def login_page():
    global is_user_logged_in
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        # Here, you should add logic to check the username and password
        # This is a simple example and should be enhanced for real-world use
        if username == "example" and password == "password":
            is_user_logged_in = True
            st.success("Successful login!")
            # After successful login, replace the content with the protected page
            content_placeholder.markdown("")  # Clear the login page content
            content_placeholder.title("Protected Page")
            content_placeholder.write("Welcome! This information is only accessible to logged-in users.")

# Main part of the program
def main():
    global is_user_logged_in

    # If the user is logged in, show the protected page
    if is_user_logged_in:
        content_placeholder.title("Protected Page")
        content_placeholder.write("Welcome! This information is only accessible to logged-in users.")
    else:
        # Otherwise, show the login page
        login_page()

if __name__ == "__main__":
    main()
