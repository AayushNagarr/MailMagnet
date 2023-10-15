import streamlit as st
import subprocess

# Define a dictionary to store user credentials (email and password)
user_credentials = {
    "user1@example.com": "password1",
    "user2@example.com": "password2",
}

# Create a Streamlit app
def main():
    st.title("Mail Magnet")

    st.sidebar.header("Navbar")

    #if authenticated i.e correct email and password redirects to home page else stays at login
    if st.session_state.is_authenticated:
        show_page("Home")
    else:
        show_page("Login")

    if st.sidebar.button("Home"):
        show_page("Home")

    if st.sidebar.button("Page 1"):
        show_page("Page 1")

    if st.sidebar.button("Page 2"):
        show_page("Page 2")

    #checks the current page and calls the corresponding function to display the content for that page
    current_page = st.session_state.page
    if current_page == "Login":
        login()
    elif current_page == "Home":
        home()
    elif current_page == "Page 1":
        page1()
    elif current_page == "Page 2":
        page2()

# Function to show a specific page i.e used to change the displayed page based on the user's selection.
def show_page(page_name):
    st.session_state.page = page_name

# Login page
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in user_credentials and user_credentials[email] == password:
            st.success("Login successful!")
            st.balloons()
            st.session_state.is_authenticated = True
            show_page("Home")

# Home page
def home():
    st.subheader("Home")
    st.write("Welcome to the home page!")
    text_input = st.text_input("Enter something:", value="")
    st.write(f"You entered: {text_input}")
    if st.button("Send to Server"):
        processed_text=send_to_server(text_input)
        st.subheader("Processed Text:")
        st.write(processed_text)

def send_to_server(text):
    try:
        # Call the other Python script and pass the text as an argument
        result= subprocess.check_output(["python", "server.py", text], text=True)
        #whole check_output is giving input and output 
        st.success("Sent to server")
        return result.strip().split("\n", 1)[1]  # Extract the second line (processed text)
    
    except subprocess.CalledProcessError as e:
        st.error(f"Error: {str(e)}")
        return "Error occurred"

# Page 1
def page1():
    st.subheader("Page 1")
    st.write("This is Page 1 content.")

# Page 2
def page2():
    st.subheader("Page 2")
    st.write("This is Page 2 content.")

if __name__ == "__main__":
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    st.session_state.page = "Login"
    main()