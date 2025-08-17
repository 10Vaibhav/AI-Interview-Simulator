from openai import OpenAI
import streamlit as st 

st.set_page_config(page_title="AI Interview Simulator", page_icon="💬")

st.title("AI Interview Simulator!")

# Build the Setup page
st.subheader("Personal Information", divider="rainbow")

name = st.text_input(label="Name", max_chars=None, placeholder="Enter your name")

experience = st.text_area(label = "Experience", value="", height=None, max_chars=None, placeholder="Describe your experience")

skills = st.text_area(label = "Skills", value="", height=None, max_chars = None, placeholder= "List your Skills")

st.write(f"**Your Name**: {name}")
st.write(f"**Your Experience**: {experience}")
st.write(f"**Your Skills**: {skills}")

st.subheader("Company and Position", divider = "rainbow")

col1, col2 = st.columns(2)

with col1:
    level = st.radio(
        "Choose level",
        key = "visibility",
        options = ["Junior", "Mid-level", "Senior"]
    )

with col2:
    position = st.selectbox(
        "Choose a position",
        ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst")
    )

company = st.selectbox(
    "Choose a Company",
    ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "Linkedin", "Spotify")
)

st.write(f"**Your Information**: {level} {position} at {company}")

# Initializing OpenAI Client
client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": f"You are an HR executive that interviews an interviewee called {name} with experience {experience} and skills {skills}. You should interview them for the position {level} {position} at the company {company}"}]

# Display the chat messages.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Implementing the Chat Functionality
if prompt := st.chat_input("Your answer."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model= st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

